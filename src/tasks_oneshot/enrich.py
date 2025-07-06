from os import getenv
import polars as pl
from config import SIRENE_DATA_DIR

def add_etablissement_data(
    df: pl.LazyFrame, etablissement_columns: list, siret_column: str
) -> pl.LazyFrame:
    """
    Ajoute les données d'établissement SIRENE à un DataFrame DECP par jointure sur le SIRET.
    - etablissement_columns : colonnes SIRENE à ajouter
    - siret_column : colonne du DataFrame DECP à utiliser pour la jointure
    Retourne un LazyFrame enrichi.
    """
    schema_etablissements = {
        "siret": "object",
        "siren": "object",
        "longitude": "float",
        "latitude": "float",
        "activitePrincipaleEtablissement": "object",
        "codeCommuneEtablissement": "object",
        "etatAdministratifEtablissement": "category",
    }
    etablissement_df_chunked = pl.scan_csv(
        getenv(f"{SIRENE_DATA_DIR}/etablissements.parquet"),
        dtype=schema_etablissements,
        index_col=None,
        usecols=["siret"] + etablissement_columns,
    )
    df = pl.merge(
        df,
        etablissement_df_chunked,
        how="inner",
        left_on="titulaire_id",
        right_on="siret",
    )
    return df

def add_unite_legale_data(
    df: pl.LazyFrame, df_sirets: pl.LazyFrame, siret_column: str, type_siret: str
) -> pl.LazyFrame:
    """
    Ajoute les données d'unité légale SIRENE à un DataFrame DECP par jointure sur le SIREN.
    - df_sirets : DataFrame contenant les SIRET à enrichir
    - siret_column : colonne SIRET à utiliser
    - type_siret : "acheteur" ou "titulaire" (pour nommer les colonnes)
    Retourne un LazyFrame enrichi.
    """
    df_sirets = df_sirets.with_columns(pl.col(siret_column).str.head(9).alias("siren"))
    unites_legales_lf = pl.scan_parquet(SIRENE_DATA_DIR + "/unites_legales.parquet")
    df_sirets = df_sirets.join(unites_legales_lf, how="inner", on="siren")
    df_sirets = df_sirets.rename(
        {"denominationUniteLegale": f"{type_siret}_nom", "siren": f"{type_siret}_siren"}
    )
    if type_siret == "acheteur":
        df = df.join(df_sirets, how="left", on="acheteur_id")
    elif type_siret == "titulaire":
        df = df.join(
            df_sirets, how="left", on=["titulaire_id", "titulaire_typeIdentifiant"]
        )
    return df
