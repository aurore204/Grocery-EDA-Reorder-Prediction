# JOJA - Turn raw data into actionable insights

[English](#-english) · [Français](#-français)

---

## English

### Project overview

Exploratory Data Analysis (EDA) of an online grocery delivery platform, based on a real anonymized dataset containing over **3 million orders** and **200,000 users**.

The goal is to identify exploitable purchasing trends and behaviors in order to propose **concrete actions to improve the business**: catalog optimization, targeted marketing, and customer retention.

### Repository structure

```
T-DAT/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies (pinned versions)
├── .gitignore
│
├── data/                              # Git-ignored (see "Getting the data")
│   ├── raw/                           # Unmodified source CSVs
│   │   ├── orders.csv
│   │   ├── order_products.csv
│   │   ├── products.csv
│   │   ├── aisles.csv
│   │   └── departments.csv
│   └── processed/                     # Auto-generated files
│       └── merged_orders.parquet
│
├── grocery_eda.ipynb                  # Final deliverable notebook
├── grocery_eda.html                   # HTML export for easy sharing
│
├── notebooks/                         # Individual exploration (not delivered)
│   ├── 01_data_loading_cleaning.ipynb
│   ├── 02_merge_feature_eng.ipynb
│   ├── 03_eda_questions_1_to_6.ipynb
│   ├── 04_eda_questions_7_to_12.ipynb
│   ├── 05_business_insights.ipynb
│   └── 06_bonus_clustering.ipynb
│
├── src/                               # Shared utility functions
│   ├── __init__.py
│   ├── data_loader.py                 # Loading, cleaning, merging tables
│   └── viz_helpers.py                 # Color palette, style, plot helpers
│
└── docs/
    ├── data_dictionary.md             # Field-level dataset documentation
    └── methodology.md                 # Methodology and tooling rationale
```

### Getting the data

The data files are not included in this repository (too large for Git). They are available on the **course Sharepoint**.

Once downloaded, place the 5 CSV files in `data/raw/`:

```
data/raw/
├── aisles.csv
├── departments.csv
├── order_products.csv
├── orders.csv
└── products.csv
```

> The `data/processed/` folder is generated automatically on the first notebook run. No need to create it manually.

### Setup

**1. Create a virtual environment** (recommended)

```bash
python -m venv venv
```

Activate it:

| System          | Command                        |
| --------------- | ------------------------------ |
| Linux / macOS   | `source venv/bin/activate`     |
| Windows         | `venv\Scripts\activate`        |

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Launch the notebook**

```bash
jupyter notebook grocery_eda.ipynb
```

### Tools

| Package        | Role                                | Why this choice                                                                      |
| -------------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| **pandas**     | Data manipulation and analysis      | De facto standard for data analysis in Python, expressive and performant API          |
| **numpy**      | Numerical computing                 | Foundation of the Python scientific ecosystem, used internally by pandas              |
| **matplotlib** | Static visualizations               | Fine-grained control over every graphical element, academic reference                 |
| **seaborn**    | Statistical visualizations          | Matplotlib wrapper with sensible aesthetic defaults and built-in statistical plots    |
| **plotly**     | Interactive visualizations          | Native interactive charts in Jupyter, ideal for data exploration                      |
| **pyarrow**    | Parquet read/write engine           | Fast and compact columnar format for caching merged data                             |
| **jupyter**    | Development environment             | Industry standard for exploratory analysis deliverables                              |

See [`docs/methodology.md`](docs/methodology.md) for a detailed rationale behind each choice.

### Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) : Field-level description of every dataset column
- [`docs/methodology.md`](docs/methodology.md) : Cleaning, merging, and analysis methodology

### Team

Hajatiana RABEMANANJARA


---

## Français

### Objectif du projet

Analyse exploratoire de données (EDA) d'un site de livraison de courses en ligne, à partir d'un dataset réel anonymisé contenant plus de **3 millions de commandes** et **200 000 utilisateurs**.

L'objectif est d'identifier des tendances et comportements d'achat exploitables, afin de proposer des **actions concrètes pour améliorer le business** : optimisation du catalogue, ciblage marketing, fidélisation client.

### Structure du repo

```
T-DAT/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python (versions épinglées)
├── .gitignore
│
├── data/                              # Ignoré par Git (voir section "Données")
│   ├── raw/                           # CSV bruts, non modifiés
│   │   ├── orders.csv
│   │   ├── order_products.csv
│   │   ├── products.csv
│   │   ├── aisles.csv
│   │   └── departments.csv
│   └── processed/                     # Fichiers générés automatiquement
│       └── merged_orders.parquet
│
├── grocery_eda.ipynb                  # Notebook final livrable
├── grocery_eda.html                   # Export HTML pour partage
│
├── notebooks/                         # Notebooks d'exploration (non livrés)
│   ├── 01_data_loading_cleaning.ipynb
│   ├── 02_merge_feature_eng.ipynb
│   ├── 03_eda_questions_1_to_6.ipynb
│   ├── 04_eda_questions_7_to_12.ipynb
│   ├── 05_business_insights.ipynb
│   └── 06_bonus_clustering.ipynb
│
├── src/                               # Fonctions utilitaires partagées
│   ├── __init__.py
│   ├── data_loader.py                 # Chargement, nettoyage, fusion des tables
│   └── viz_helpers.py                 # Palette, style, fonctions de visualisation
│
└── docs/
    ├── data_dictionary.md             # Description de chaque champ
    └── methodology.md                 # Méthodologie et justification des outils
```

### Récupérer les données

Les fichiers de données ne sont pas inclus dans ce repo (trop volumineux pour Git). Ils sont disponibles sur le **Sharepoint du cours**.

Une fois téléchargés, placez les 5 fichiers CSV dans `data/raw/` :

```
data/raw/
├── aisles.csv
├── departments.csv
├── order_products.csv
├── orders.csv
└── products.csv
```

> Le dossier `data/processed/` est généré automatiquement au premier lancement du notebook. Il n'est pas nécessaire de le créer manuellement.

### Installation

**1. Créer un environnement virtuel** (recommandé)

```bash
python -m venv venv
```

Activer l'environnement :

| Système         | Commande                       |
| --------------- | ------------------------------ |
| Linux / macOS   | `source venv/bin/activate`     |
| Windows         | `venv\Scripts\activate`        |

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Lancer le notebook**

```bash
jupyter notebook grocery_eda.ipynb
```

### Outils utilisés

| Package        | Rôle                                      | Pourquoi ce choix                                                                 |
| -------------- | ----------------------------------------- | --------------------------------------------------------------------------------- |
| **pandas**     | Manipulation et analyse des données       | Standard de facto pour la data analysis en Python, API expressive et performante   |
| **numpy**      | Calcul numérique                          | Fondation de l'écosystème scientifique Python, utilisé en interne par pandas       |
| **matplotlib** | Visualisations statiques                  | Contrôle fin sur chaque élément graphique, référence académique                   |
| **seaborn**    | Visualisations statistiques               | Surcouche de matplotlib avec des defaults esthétiques et des graphes statistiques  |
| **plotly**     | Visualisations interactives               | Graphiques interactifs natifs dans Jupyter, idéal pour l'exploration               |
| **pyarrow**    | Moteur de lecture/écriture Parquet        | Format colonnaire rapide et compact pour le cache des données fusionnées           |
| **jupyter**    | Environnement de développement            | Standard pour les livrables d'analyse exploratoire                                |

Voir [`docs/methodology.md`](docs/methodology.md) pour une justification détaillée de chaque choix.

### Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) : Description de chaque champ des datasets
- [`docs/methodology.md`](docs/methodology.md) : Méthodologie de nettoyage, fusion et analyse

### Équipe

Hajatiana RABEMANANJARA