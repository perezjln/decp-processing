import os
import sqlite3
import polars as pl
from config import DIST_DIR

def save_to_files(df: pl.DataFrame, path: str, file_format=None):
    """
    Sauvegarde un DataFrame Polars au format CSV et/ou Parquet.
    - df : DataFrame à sauvegarder
    - path : chemin de base (sans extension)
    - file_format : liste des formats à écrire (par défaut ["csv", "parquet"])
    """
    if file_format is None:
        file_format = ["csv", "parquet"]
    if "csv" in file_format:
        df.write_csv(f"{path}.csv")
    if "parquet" in file_format:
        df.write_parquet(f"{path}.parquet")

def save_to_sqlite(df: pl.DataFrame, database: str, table_name: str, primary_key: str):
    """
    Sauvegarde un DataFrame Polars dans une base SQLite.
    - database : nom du fichier sqlite (sans extension)
    - table_name : nom de la table à créer
    - primary_key : clé primaire (simple ou composite)
    """
    # Suppression des doublons selon la clé primaire (polars)
    subset_cols = [col.strip().replace('"', '').replace("'", '') for col in primary_key.split(",")]
    df = df.unique(subset=subset_cols)

    column_definitions = []
    for column_name, column_type in zip(df.columns, df.dtypes):
        sql_type = "TEXT"
        if column_type in [pl.Int16, pl.Int64, pl.Boolean]:
            sql_type = "INTEGER"
        elif column_type in [pl.Float32, pl.Float64]:
            sql_type = "REAL"
        column_definitions.append(f'"{column_name}" {sql_type}')

    if "." in primary_key and '"' not in primary_key:
        raise ValueError(
            f"Les noms de colonnes contenant un point doivent être entre guillemets : {primary_key}"
        )

    primary_key_definition = f"PRIMARY KEY({primary_key})"
    create_table_sql = f'CREATE TABLE "{table_name}" ({", ".join(column_definitions)}, {primary_key_definition})'

    connection = sqlite3.connect(f"{DIST_DIR}/{database}.sqlite")
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()

    df.write_database(
        f'"{table_name}"',
        f"sqlite:///{DIST_DIR}/{database}.sqlite",
        if_table_exists="append",
    )
