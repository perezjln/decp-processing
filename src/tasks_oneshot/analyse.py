import os
from datetime import datetime
import polars as pl
from config import DATE_NOW
from tasks_oneshot.setup import create_table_artifact

def list_data_issues(df: pl.LazyFrame):
    df = df.collect()
    date_columns = [
        "dateNotification",
        "dateNotificationActeSousTraitance",
        "dateNotificationModificationModification",
        "dateNotificationModificationSousTraitanceModificationActeSousTraitance",
        "datePublicationDonnees",
        "datePublicationDonneesActeSousTraitance",
        "datePublicationDonneesModificationActeSousTraitance",
        "datePublicationDonneesModificationModification",
    ]
    for column in date_columns:
        print(
            "Dates impossibles dans la colonne ",
            column,
            ":",
            df.filter(
                (pl.col(column) < pl.date(2015, 1, 1))
                | (pl.col(column) > datetime.now())
            ).height,
        )

def generate_stats(df: pl.DataFrame):
    now = datetime.now()
    df_uid: pl.DataFrame = df.select(
        "uid", "acheteur_id", "datePublicationDonnees", "dateNotification", "montant"
    ).unique(subset=["uid"])
    stats = {
        "datetime": now.isoformat()[:-7],
        "date": DATE_NOW,
        "fichiers": os.environ.get("downloaded_files", "").split(","),
        "nb_lignes": df.height,
        "colonnes_triées": sorted(df.columns),
        "nb_colonnes": len(df.columns),
        "nb_marches": df_uid.height,
        "nb_acheteurs_uniques": df_uid.select("acheteur_id").unique().height - 1,
        "nb_titulaires_uniques": df.select("titulaire_id", "titulaire_typeIdentifiant").unique().height - 1,
    }
    for year in range(2018, int(DATE_NOW[0:4]) + 1):
        stats[f"{str(year)}_nb_publications_marchés"] = df_uid.filter(
            pl.col("datePublicationDonnees").dt.year() == year
        ).height
    print("[STATS]", stats)
    create_table_artifact(
        table=[stats],
        key="decp-stats",
        description=f"Statistiques sur les DECP ({DATE_NOW})",
    )
