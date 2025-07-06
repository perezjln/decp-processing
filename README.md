# DECP Processing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Polars](https## Tests & Qualité

- **Tests unitaires** :
  ```bash
  pytest
  ```
- **Linting & formatage** :
  ```bash
  pre-commit run --all-files
  ```

- **Variables d'environnement de test** configurées dans `pyproject.toml`
- **Données de test** disponibles dans le répertoire `data/`img.shields.io/badge/polars-1.27.0-blue.svg)](https://pola-rs.github.io/polars/)

**DECP Processing** est un pipeline open source pour le traitement, la normalisation et la publication des données essentielles de la commande publique (DECP) en France. Il vise à rendre ces données plus accessibles, fiables et exploitables pour tous : entreprises, journalistes, chercheurs, citoyens, acteurs publics.

---

## Sommaire

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Données produites](#données-produites)
- [Installation](#installation)
  - [Environnement local](#environnement-local)
  - [Docker](#docker)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Tests & Qualité](#tests--qualité)
- [Contribuer](#contribuer)
- [Ressources & Liens](#ressources--liens)
- [Licence](#licence)

---

## Présentation

Le projet répond à la complexité et au manque d'ouverture du pipeline officiel du Ministère des Finances pour la publication des DECP. Il propose une alternative transparente, documentée et collaborative, adaptée aux besoins des utilisateurs.

- Code source d’agrégation officiel : [fermé](https://github.com/139bercy/decp-rama-v2)
- Documentation officielle : [éparpillée et incomplète](https://www.data.gouv.fr/fr/datasets/5cd57bf68b4c4179299eb0e9)
- Schéma DECP complexe à exploiter

**DECP Processing** simplifie, enrichit et publie ces données dans des formats modernes (CSV, Parquet, SQLite).

---

## Fonctionnalités

- **Téléchargement automatisé** : Récupération des données DECP consolidées depuis data.gouv.fr
- **Nettoyage et normalisation** : Traitement des données JSON sources, typage des colonnes
- **Enrichissement SIRENE** : Ajout automatique des données d'entreprises (unités légales)
- **Exports multi-formats** : 
  - CSV et Parquet pour l'analyse
  - SQLite pour les applications datalab
  - Données avec/sans informations titulaires
- **Publication automatisée** : Mise à jour directe sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-consolidees-format-tabulaire/)
- **Pipeline flexible** : Mode "oneshot" sans dépendances ou avec Prefect
- **Containerisation** : Support Docker complet
- **Qualité** : Tests unitaires et outils de qualité de code

---

## Données produites

- **Source** : Données consolidées du Ministère des Finances ([data.gouv.fr](https://www.data.gouv.fr/fr/datasets/5cd57bf68b4c4179299eb0e9))
- **Période couverte** : Données mensuelles depuis 2019 (actuellement jusqu'à mai 2025)
- **Formats disponibles** : 
  - CSV et Parquet (données complètes)
  - SQLite (base normalisée pour datalab)
  - Version anonymisée sans titulaires
- **Enrichissement** : Données SIRENE automatiquement ajoutées
- **Téléchargement** :
  - [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-consolidees-format-tabulaire/)
  - [decp.info](https://decp.info) (visualisation, filtrage, téléchargement)

---

## Installation

### Environnement local

1. **Prérequis** :
   - Python 3.8+ (testé avec Python 3.12)
   - [Rust/Cargo](https://rustup.rs) (requis pour Polars)
   - [pip](https://pip.pypa.io/)

2. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/ColinMaudry/decp-processing.git
   cd decp-processing
   ```

3. **Créer un environnement virtuel** :
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```

4. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   # ou pour installer avec les dépendances de développement
   pip install -e .[dev]
   ```

5. **Configurer l'environnement** :
   ```bash
   cp template.env .env
   # Éditez .env selon vos besoins (chemins, clés API, etc.)
   ```

### Docker

1. **Construire et lancer le conteneur** :
   ```bash
   docker build -t decp-processing .
   docker run --rm -it -v ${PWD}:/app decp-processing
   ```

2. **Avec variables d'environnement** :
   ```bash
   docker run --rm -it -v ${PWD}:/app --env-file .env decp-processing
   ```

---

## Utilisation

### Pipeline complet (mode oneshot)
```bash
python src/flows_oneshot.py
```

### Fonctions spécifiques

#### Préparation des données SIRENE uniquement
```bash
python -c "from src.flows_oneshot import sirene_preprocess; sirene_preprocess()"
```

#### Nettoyage et fusion des données DECP
```bash
python -c "from src.flows_oneshot import get_clean_concat; get_clean_concat()"
```

#### Génération des fichiers pour decp.info
```bash
python -c "from src.flows_oneshot import make_decpinfo_data; make_decpinfo_data()"
```

#### Création de la base SQLite datalab
```bash
python -c "from src.flows_oneshot import make_datalab_data; make_datalab_data()"
```

### Personnalisation
- Modifiez le fichier `.env` pour :
  - Pointer vers vos propres sources de données
  - Configurer les chemins de sortie
  - Activer/désactiver la publication automatique
  - Configurer les clés API data.gouv.fr

---

## Configuration

### Fichiers de configuration

- **`.env`** : Variables d'environnement principales
  - `DECP_JSON_FILES_PATH` : Chemin vers la liste des fichiers JSON à traiter
  - `DECP_DIST_DIR` : Répertoire de sortie des fichiers générés
  - `DECP_PROCESSING_PUBLISH` : Activer/désactiver la publication automatique
  - `DATAGOUVFR_API_KEY` : Clé API pour publication sur data.gouv.fr
  - `SIRENE_DATA_DIR` : Répertoire pour les données SIRENE

- **`data/decp_json_files.json`** : Configuration des fichiers sources à traiter
- **`pyproject.toml`** : Dépendances Python et configuration des outils
- **`requirements.txt`** : Dépendances principales

### Structure des données

Le pipeline traite les colonnes suivantes :
- Identifiants : `uid`, `id`, `nature`
- Acheteurs : `acheteur_id`, `acheteur_nom`, `acheteur_siren`
- Titulaires : `titulaire_id`, `titulaire_nom`, `titulaire_siren`
- Marché : `objet`, `montant`, `codeCPV`, `procedure`, `dureeMois`
- Dates : `dateNotification`, `datePublicationDonnees`
- Autres : `formePrix`, `lieuExecution_code`, etc.

---

## Architecture du projet

```
├── src/
│   ├── config.py              # Configuration centrale
│   ├── flows_oneshot.py       # Pipeline principal
│   ├── extract_sql_schema.py  # Extraction schéma SQL
│   └── tasks_oneshot/         # Modules de traitement
│       ├── get.py            # Téléchargement des données
│       ├── clean.py          # Nettoyage et validation
│       ├── transform.py      # Transformation et fusion
│       ├── enrich.py         # Enrichissement SIRENE
│       ├── analyse.py        # Génération de statistiques
│       ├── output.py         # Export des formats
│       └── publish.py        # Publication data.gouv.fr
├── data/                     # Données sources et test
├── dist/                     # Fichiers générés (créé automatiquement)
├── drawings/                 # Schémas et diagrammes
└── requirements.txt          # Dépendances
```

---

## Contribuer

Les contributions sont bienvenues !  
Merci de lire le [CONTRIBUTING.md](CONTRIBUTING.md) s’il existe, ou d’ouvrir une issue pour toute question.

- Forkez le projet
- Créez une branche (`git checkout -b feature/ma-fonction`)
- Commitez vos modifications
- Ouvrez une Pull Request

---

## Contribuer

Les contributions sont bienvenues !

- [Documentation officielle DECP](https://data.economie.gouv.fr/pages/donnees-essentielles-de-la-commande-publique/)
- [Schéma DECP](https://github.com/ColinMaudry/decp-table-schema)
- [SIRENE Open Data](https://www.data.gouv.fr/fr/datasets/r/0835cd60-2c2a-497b-bc64-404de704ce89)
- [Polars Documentation](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)
- [Frictionless Data](https://frictionlessdata.io/)
- [API data.gouv.fr](https://doc.data.gouv.fr/api/)

---

## Licence

Ce projet est sous licence MIT.  
© Colin Maudry et contributeurs.

---

**Version** : 0.1.1  
**Dernière mise à jour** : Juillet 2025

*Pour toute question, ouvrez une issue ou contactez [colin+decp@maudry.com](mailto:colin+decp@maudry.com).*
