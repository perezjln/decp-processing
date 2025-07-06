def create_table_artifact(table, key: str, description: str = None):
    """
    Simule la création d'un artefact de suivi (tableau de stats, logs, etc).
    Dans le mode oneshot, affiche simplement un résumé dans la console.
    - table : liste de dicts (lignes)
    - key : identifiant de l'artefact
    - description : description optionnelle
    """
    # In oneshot mode, just print or log the artifact info, or pass
    print(f"[ARTIFACT] key={key}, description={description}, rows={len(table)}")
    # You could also write to a file or database if needed
