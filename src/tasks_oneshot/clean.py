import os
import polars as pl
from config import DIST_DIR
from tasks_oneshot.output import save_to_files
from tasks_oneshot.transform import explode_titulaires

def clean_decp_json(files: list):
    return_files = []
    for file in files:
        lf: pl.LazyFrame = pl.scan_parquet(f"{file}.parquet")
        print("Explode titulaires...")
        lf = explode_titulaires(lf)
        lf = lf.with_columns(pl.col(pl.String).replace("NC", None))
        lf = lf.with_columns(pl.col("id").str.replace_all(r"[ ,\\./]", "_"))
        lf = lf.with_columns((pl.col("acheteur_id") + pl.col("id")).alias("uid"))
        date_replacements = {
            "0002-11-30": "",
            "September, 16 2021 00:00:00": "2021-09-16",
            "16 2021 00:00:00": "",
            "0222-04-29": "2022-04-29",
            "0021-12-05": "2022-12-05",
            "0001-06-21": "",
            "0019-10-18": "",
            "5021-02-18": "2021-02-18",
            "2921-11-19": "",
            "0022-04-29": "2022-04-29",
        }
        lf = lf.with_columns(
            pl.col(["datePublicationDonnees", "dateNotification"])
            .str.replace_many(date_replacements)
            .cast(pl.Utf8)
        )
        lf = lf.with_columns(
            pl.col("nature").str.replace_many({"Marche": "Marché", "subsequent": "subséquent"})
        )
        lf = fix_data_types(lf)
        file = f"{DIST_DIR}/clean/{file.split('/')[-1]}"
        return_files.append(file)
        if not os.path.exists(f"{DIST_DIR}/clean"):
            os.mkdir(f"{DIST_DIR}/clean")
        df: pl.DataFrame = lf.collect()
        save_to_files(df, file, ["parquet"])
    return return_files

def fix_data_types(df: pl.LazyFrame):
    numeric_dtypes = {
        "dureeMois": pl.Int16,
        "offresRecues": pl.Int16,
        "montant": pl.Float64,
        "tauxAvance": pl.Float64,
    }
    for column, dtype in numeric_dtypes.items():
        print("Fixing column", column, "...")
        df = df.with_columns(pl.col(column).cast(dtype, strict=False))
    print("Fixing dates...")
    df = df.with_columns(
        pl.col([
            "dateNotification",
            "datePublicationDonnees",
        ]).str.strptime(pl.Date, format="%Y-%m-%d", strict=False)
    )
    return df
