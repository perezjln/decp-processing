import os.path
import shutil

import polars as pl

from config import BASE_DF_COLUMNS, DECP_PROCESSING_PUBLISH, DIST_DIR, SIRENE_DATA_DIR
from tasks_oneshot.analyse import generate_stats
from tasks_oneshot.clean import clean_decp_json
from tasks_oneshot.enrich import add_unite_legale_data
from tasks_oneshot.get import get_decp_json
from tasks_oneshot.output import (
    save_to_files,
    save_to_sqlite,
)
from tasks_oneshot.publish import publish_to_datagouv
from tasks_oneshot.transform import (
    concat_decp_json,
    extract_unique_acheteurs_siret,
    extract_unique_titulaires_siret,
    get_prepare_unites_legales,
    make_decp_sans_titulaires,
    normalize_tables,
    sort_columns,
)


def get_clean_concat():
    """
    Nettoie, fusionne et enrichit les données DECP, puis les enregistre aux formats CSV et Parquet.
    Retourne le DataFrame final prêt pour les traitements suivants.
    """
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.mkdir(DIST_DIR)

    # Vérifie et prépare les données SIRENE si besoin
    if not os.path.exists(SIRENE_DATA_DIR + "/unites_legales.parquet"):
        print("Prétraitement SIRENE nécessaire...")
        sirene_preprocess()

    print("Récupération des données source...")
    files = get_decp_json()

    print("Nettoyage des données source et typage des colonnes...")
    files = clean_decp_json(files)

    print("Fusion des dataframes...")
    df = concat_decp_json(files)

    print("Ajout des données SIRENE...")
    lf = enrich_from_sirene(df.lazy())

    print("Génération de l'artefact (statistiques) sur le base df...")
    df = lf.collect(engine="streaming")
    generate_stats(df)

    print("Enregistrement des DECP aux formats CSV, Parquet...")
    df = sort_columns(df, BASE_DF_COLUMNS)
    save_to_files(df, f"{DIST_DIR}/decp")
    return df


def make_datalab_data():
    """
    Crée la base SQLite pour le datalab à partir du fichier Parquet principal,
    puis normalise les tables et publie éventuellement sur data.gouv.fr.
    """
    df = pl.read_parquet(f"{DIST_DIR}/decp.parquet")

    print("Enregistrement des DECP aux formats SQLite...")
    save_to_sqlite(
        df,
        "datalab",
        "data.gouv.fr.2022.clean",
        "uid, titulaire_id, titulaire_typeIdentifiant",
    )

    print("Normalisation des tables...")
    normalize_tables(df)

    if DECP_PROCESSING_PUBLISH.lower() == "true":
        print("Publication sur data.gouv.fr...")
        publish_to_datagouv(context="datalab")
    else:
        print("Publication sur data.gouv.fr désactivée.")


def make_decpinfo_data():
    """
    Génère les fichiers DECP sans titulaires, prépare le data package (optionnel),
    et publie éventuellement sur data.gouv.fr.
    """
    df = pl.read_parquet(f"{DIST_DIR}/decp.parquet")

    # DECP sans titulaires
    save_to_files(make_decp_sans_titulaires(df), f"{DIST_DIR}/decp-sans-titulaires")

    # print("Ajout des colonnes manquantes...")
    # df = setup_tableschema_columns(df)

    # CREATION D'UN DATA PACKAGE (FRICTIONLESS DATA)
    # Pas la priorité pour le moment, prend du temps
    # print("Validation des données DECP avec le TableSchema...")
    # validate_decp_against_tableschema()
    # print("Création du data package (JSON)....")
    # make_data_package()

    # PUBLICATION DES FICHIERS SUR DATA.GOUV.FR
    if DECP_PROCESSING_PUBLISH.lower() == "true":
        print("Publication sur data.gouv.fr...")
        publish_to_datagouv(context="decp")
    else:
        print("Publication sur data.gouv.fr désactivée.")
    return df


def enrich_from_sirene(df: pl.LazyFrame):
    """
    Ajoute les données SIRENE (unités légales) aux acheteurs et titulaires présents dans le DataFrame.
    """
    assert os.path.exists(SIRENE_DATA_DIR + "/unites_legales.parquet")

    print("Extraction des SIRET des acheteurs...")
    df_sirets_acheteurs = extract_unique_acheteurs_siret(df.clone())
    print("Ajout des données unités légales (acheteurs)...")
    df = add_unite_legale_data(
        df, df_sirets_acheteurs, siret_column="acheteur_id", type_siret="acheteur"
    )

    print("Extraction des SIRET des titulaires...")
    df_sirets_titulaires = extract_unique_titulaires_siret(df)
    print("Ajout des données unités légales (titulaires)...")
    df = add_unite_legale_data(
        df, df_sirets_titulaires, siret_column="titulaire_id", type_siret="titulaire"
    )
    return df


def sirene_preprocess():
    """
    Prépare les données SIRENE (unités légales) si elles ne sont pas déjà présentes.
    """
    sirene_data_dir = SIRENE_DATA_DIR
    print("SIRENE directory: " + sirene_data_dir)

    if not os.path.exists(sirene_data_dir):
        os.mkdir(sirene_data_dir)

    # préparer les données unités légales
    print("Prépararion des unités légales...")
    get_prepare_unites_legales()


def main():
    """
    Point d'entrée principal : lance le prétraitement SIRENE, la fusion/nettoyage des données,
    la génération des fichiers DECP, la création de la base datalab et la publication.
    """
    
    # Prétraitement des données SIRENE
    sirene_preprocess()
    
    # Données nettoyées et fusionnées
    get_clean_concat()
    
    # Fichiers dédiés à l'Open Data et decp.info
    make_decpinfo_data()
    
    # Base de données SQLite dédiée aux activités du Datalab d'Anticor
    make_datalab_data()

if __name__ == "__main__":
    main()
