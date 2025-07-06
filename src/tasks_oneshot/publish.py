from os import getenv
from httpx import post
from config import DIST_DIR

def update_resource(api, dataset_id, resource_id, file_path, api_key):
    """
    Met à jour une ressource data.gouv.fr via l'API (upload d'un fichier).
    - api : URL de l'API
    - dataset_id : identifiant du dataset
    - resource_id : identifiant de la ressource
    - file_path : chemin du fichier à uploader
    - api_key : clé API data.gouv.fr
    Retourne la réponse JSON de l'API.
    """
    url = f"{api}/datasets/{dataset_id}/resources/{resource_id}/upload/"
    headers = {"X-API-KEY": api_key}
    file = {"file": open(file_path, "rb")}
    response = post(url, files=file, headers=headers, timeout=120)
    return response.json()

def publish_to_datagouv(context: str):
    """
    Publie les fichiers produits sur data.gouv.fr selon le contexte ("decp" ou "datalab").
    Nécessite une clé API data.gouv.fr dans l'environnement.
    """
    api_key = getenv("DATAGOUVFR_API_KEY")
    api = "https://www.data.gouv.fr/api/1"
    dataset_id = "608c055b35eb4e6ee20eb325"
    uploads = [
        {
            "file": f"{DIST_DIR}/decp.parquet",
            "resource_id": "11cea8e8-df3e-4ed1-932b-781e2635e432",
            "context": context,
        },
        {
            "file": f"{DIST_DIR}/decp-sans-titulaires.csv",
            "resource_id": "834c14dd-037c-4825-958d-0a841c4777ae",
            "context": "decp",
        },
        {
            "file": f"{DIST_DIR}/decp-sans-titulaires.parquet",
            "resource_id": "df28fa7d-2d36-439b-943a-351bde02f01d",
            "context": "decp",
        },
        {
            "file": f"{DIST_DIR}/datalab.sqlite",
            "resource_id": "43f54982-da60-4eb7-aaaf-ba935396209b",
            "context": "datalab",
        },
    ]
    for upload in uploads:
        if upload["context"] == context:
            print(f"Uploading {upload['file']} to DataGouv resource {upload['resource_id']}...")
            update_resource(api, dataset_id, upload["resource_id"], upload["file"], api_key)
