import polars as pl

def explode_titulaires(df: pl.LazyFrame):
    df = df.explode("titulaires")
    df = df.select(
        pl.col("*"),
        pl.col("titulaires")
        .struct.rename_fields(["titulaires.object"])
        .alias("titulaires_renamed"),
    )
    df = df.unnest("titulaires_renamed")
    df = df.select(
        pl.col("*"),
        pl.col("titulaires.object")
        .struct.rename_fields(["titulaire_typeIdentifiant", "titulaire_id"])
        .alias("titulaire"),
    )
    df = df.unnest("titulaire")
    df = df.drop(["titulaires", "titulaires.object"])
    df = df.with_columns(pl.col("titulaire_id").cast(pl.String))
    df = df.with_columns([
        pl.when(pl.col("titulaire_typeIdentifiant").str.contains(r"[0-9]"))
        .then(pl.col("titulaire_id"))
        .otherwise(pl.col("titulaire_typeIdentifiant"))
        .alias("titulaire_typeIdentifiant"),
        pl.when(pl.col("titulaire_typeIdentifiant").str.contains(r"[0-9]"))
        .then(pl.col("titulaire_typeIdentifiant"))
        .otherwise(pl.col("titulaire_id"))
        .alias("titulaire_id"),
    ])
    return df

def concat_decp_json(files: list) -> pl.DataFrame:
    dfs = []
    all_columns = set()
    dtypes = {}
    # Première passe : collecter tous les noms de colonnes et types
    for file in files:
        df = pl.read_parquet(f"{file}.parquet")
        dfs.append(df)
        for col, dtype in zip(df.columns, df.dtypes):
            all_columns.add(col)
            # On garde le type le plus fréquent ou le plus général (ici, String par défaut)
            if col not in dtypes:
                dtypes[col] = dtype
            elif dtypes[col] != dtype:
                dtypes[col] = pl.String
    all_columns = list(all_columns)
    # Deuxième passe : aligner les colonnes et types
    aligned_dfs = []
    for df in dfs:
        for col in all_columns:
            if col not in df.columns:
                df = df.with_columns(pl.lit(None, dtype=dtypes[col]).alias(col))
        # Cast toutes les colonnes au type choisi
        df = df.select([pl.col(col).cast(dtypes[col], strict=False) for col in all_columns])
        aligned_dfs.append(df)
    df = pl.concat(aligned_dfs, how="diagonal")
    print(
        "Suppression des lignes en doublon par UID + titulaire ID + titulaire type ID"
    )
    index_size_before = df.height
    df = df.unique(
        subset=["uid", "titulaire_id", "titulaire_typeIdentifiant"],
        maintain_order=False,
    )
    print("-- ", index_size_before - df.height, " doublons supprimés")
    return df

def extract_unique_acheteurs_siret(df: pl.LazyFrame):
    df = df.select("acheteur_id")
    df = df.unique().filter(pl.col("acheteur_id") != "")
    df = df.sort(by="acheteur_id")
    return df

def extract_unique_titulaires_siret(df: pl.LazyFrame):
    df = df.select("titulaire_id", "titulaire_typeIdentifiant")
    df = df.unique().filter(
        pl.col("titulaire_id") != "", pl.col("titulaire_typeIdentifiant") == "SIRET"
    )
    df = df.sort(by="titulaire_id")
    return df

def make_decp_sans_titulaires(df: pl.DataFrame):
    df_decp_sans_titulaires = df.drop([
        "titulaire_id",
        "titulaire_typeIdentifiant",
    ])
    df_decp_sans_titulaires = df_decp_sans_titulaires.unique()
    return df_decp_sans_titulaires

def normalize_tables(df):
    df_marches: pl.DataFrame = pl.DataFrame(df.to_arrow()).drop(
        "titulaire_id", "titulaire_typeIdentifiant"
    )
    df_marches = df_marches.unique("uid").sort(
        by="datePublicationDonnees", descending=True
    )
    from tasks_oneshot.output import save_to_sqlite
    save_to_sqlite(df_marches, "datalab", "marches", "uid")
    del df_marches
    df_acheteurs: pl.DataFrame = df.select("acheteur_id")
    df_acheteurs = df_acheteurs.rename({"acheteur_id": "id"})
    df_acheteurs = df_acheteurs.unique().sort(by="id")
    save_to_sqlite(df_acheteurs, "datalab", "acheteurs", "id")
    del df_acheteurs
    df_titulaires: pl.DataFrame = df.select("titulaire_id", "titulaire_typeIdentifiant")
    df_titulaires = df_titulaires.rename(
        {"titulaire_id": "id", "titulaire_typeIdentifiant": "typeIdentifiant"}
    )
    df_titulaires = df_titulaires.unique().sort(by=["id"])
    save_to_sqlite(df_titulaires, "datalab", "entreprises", "id, typeIdentifiant")
    del df_titulaires
    df_marches_titulaires: pl.DataFrame = df.select(
        "uid", "titulaire_id", "titulaire_typeIdentifiant"
    )
    df_marches_titulaires = df_marches_titulaires.rename({"uid": "marche_uid"})
    save_to_sqlite(
        df_marches_titulaires,
        "datalab",
        "marches_titulaires",
        '"marche_uid", "titulaire_id", "titulaire_typeIdentifiant"',
    )
    del df_marches_titulaires

def sort_columns(df: pl.DataFrame, config_columns):
    other_columns = []
    for col in df.columns:
        if col not in config_columns:
            other_columns.append(col)
    print("Colonnes inattendues:", other_columns)
    return df.select(config_columns + other_columns)

def get_prepare_unites_legales():
    import os
    import zipfile
    from httpx import get
    from config import SIRENE_DATA_DIR
    sirene_data_dir = SIRENE_DATA_DIR
    unites_legales_path = f"{sirene_data_dir}/StockUniteLegale_utf8"
    if not os.path.exists(f"{unites_legales_path}.zip"):
        print("Téléchargement des unités légales...")
        unites_legales_url = os.getenv("SIRENE_UNITES_LEGALES_URL")
        request = get(unites_legales_url, follow_redirects=True)
        with open(f"{unites_legales_path}.zip", "wb") as file:
            file.write(request.content)
    if not any(f.endswith('.csv') for f in os.listdir(sirene_data_dir)):
        print("Décompression des unités légales...")
        with zipfile.ZipFile(f"{unites_legales_path}.zip", "r") as zip_ref:
            zip_ref.extractall(sirene_data_dir)
    # Recherche du vrai nom du .csv extrait
    csv_files = [f for f in os.listdir(sirene_data_dir) if f.endswith('.csv') and 'UniteLegale' in f]
    if not csv_files:
        raise FileNotFoundError("Aucun fichier CSV d'unités légales trouvé après extraction.")
    csv_path = os.path.join(sirene_data_dir, csv_files[0])
    print(f"Utilisation du fichier CSV: {csv_path}")
    import polars as pl
    lf_ul = pl.scan_csv(csv_path, infer_schema=None)
    lf_ul = lf_ul.select(["siren", "denominationUniteLegale"])
    lf_ul = lf_ul.sort(by="siren")
    lf_ul.collect(engine="streaming").write_parquet(
        f"{sirene_data_dir}/unites_legales.parquet"
    )
