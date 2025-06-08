import sqlite3

# Remplacez ce chemin si besoin
db_path = "dist/datalab.sqlite"
output_path = "datalab_schema.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Récupère la liste des tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

with open(output_path, "w", encoding="utf-8") as f:
    for table in tables:
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
        create_stmt = cursor.fetchone()[0]
        f.write(f"{create_stmt};\n\n")

conn.close()
print(f"Schéma exporté dans {output_path}")