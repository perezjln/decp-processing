def create_table_artifact(table, key: str, description: str = None):
    # In oneshot mode, just print or log the artifact info, or pass
    print(f"[ARTIFACT] key={key}, description={description}, rows={len(table)}")
    # You could also write to a file or database if needed
