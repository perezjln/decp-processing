# DECP Processing

[![Tests](https://img.shields.io/github/workflow/status/ColinMaudry/decp-processing/CI/main?label=tests)](https://github.com/ColinMaudry/decp-processing/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

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

- Téléchargement automatisé des DECP consolidées
- Nettoyage, normalisation et enrichissement (SIRENE, SIRET, etc.)
- Export multi-formats : CSV, Parquet, SQLite
- Publication automatisée sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-consolidees-format-tabulaire/)
- Pipeline reproductible (Prefect ou mode "oneshot" sans dépendance)
- Compatible Docker
- Tests unitaires et outils de qualité de code

---

## Données produites

- **Source** : Données consolidées du Ministère des Finances ([data.gouv.fr](https://www.data.gouv.fr/fr/datasets/5cd57bf68b4c4179299eb0e9))
- **Formats** : CSV, Parquet, SQLite
- **Téléchargement** :
  - [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-consolidees-format-tabulaire/)
  - [decp.info](https://decp.info) (visualisation, filtrage, téléchargement)

---

## Installation

### Environnement local

1. **Prérequis** :
   - Python 3.8+
   - [Rust/Cargo](https://rustup.rs) (pour Polars)
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
   pip install .[dev]  # Pour les outils de dev (optionnel)
   ```

5. **Configurer l'environnement** :
   ```bash
   cp template.env .env
   # Éditez .env selon vos besoins (chemins, clés API, etc.)
   ```

### Docker

1. **Construire et lancer le conteneur** :
   ```powershell
   ./script/docker_build_and_run.bat
   ```
   ou en ligne de commande :
   ```bash
   docker build -t decp_preprocessing .
   docker run --rm -it -v ${PWD}:/app -p 4200:4200 decp_preprocessing
   ```

---

## Utilisation

### Pipeline complet (mode Prefect)
```bash
python src/flows.py
```

### Pipeline rapide (mode oneshot, sans Prefect)
```bash
python src/flows_oneshot.py
```

### Lancer un traitement SIRENE seul
```bash
python src/flows_oneshot.py sirene_preprocess
```

### Personnalisation
- Modifiez le fichier `.env` pour pointer vers vos propres sources ou modifier les options de publication.

---

## Configuration

- `.env` : variables d'environnement (chemins, clés API, options de publication)
- `pyproject.toml` : dépendances, options de test, etc.
- `requirements.txt` : dépendances principales

---

## Tests & Qualité

- **Tests unitaires** :
  ```bash
  pytest
  ```
- **Linting & formatage** :
  ```bash
  pre-commit run --all-files
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

## Ressources & Liens

- [Documentation officielle DECP](https://data.economie.gouv.fr/pages/donnees-essentielles-de-la-commande-publique/)
- [Schéma DECP](https://github.com/ColinMaudry/decp-table-schema)
- [SIRENE Open Data](https://www.data.gouv.fr/fr/datasets/r/5e4b7e9c634f411f8b8b4567)
- [Polars](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)
- [Prefect](https://docs.prefect.io/)

---

## Licence

Ce projet est sous licence MIT.  
© Colin Maudry et contributeurs.

---

*Pour toute question, ouvrez une issue ou contactez [colin+decp@maudry.com](mailto:colin+decp@maudry.com).*
