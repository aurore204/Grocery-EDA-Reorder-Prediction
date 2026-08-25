# JOJA — Turn Ordinary Data Into Insights

## Objectif du projet

Analyse exploratoire de données (EDA) d'un site de livraison de courses en ligne, à partir d'un dataset réel de plus de 3 millions de commandes et 200 000 utilisateurs. L'objectif est d'identifier des tendances et comportements d'achat exploitables, afin de proposer des actions concrètes pour améliorer le business.

## Structure du repo

grocery-data-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   ├── orders.csv
│   │   ├── order_products.csv
│   │   ├── products.csv
│   │   ├── aisles.csv
│   │   └── departments.csv
│   └── processed/
│       └── merged_orders.parquet
│
├── grocery_eda.ipynb
├── grocery_eda.html
│
├── notebooks/non livré— exploration individuelle
│   ├── 01_data_loading_cleaning.ipynb
│   ├── 02_merge_feature_eng.ipynb
│   ├── 03_eda_questions_1_to_6.ipynb
│   ├── 04_eda_questions_7_to_12.ipynb
│   ├── 05_business_insights.ipynb
│   └── 06_bonus_clustering.ipynb— bonus avancé
│
├── src/— fonctions utilitaires importables
│   ├── __init__.py
│   ├── data_loader.py
│   └── viz_helpers.py
│
└── docs/
    ├── data_dictionary
    └── methodology



## 📊 Récupérer les données

Les fichiers de données ne sont pas inclus dans ce repo (trop volumineux pour GitHub). Ils sont disponibles sur le **Sharepoint du cours C-DEV-120**.

Une fois téléchargés, placez les 5 fichiers CSV dans `data/raw/` :

data/raw/
├── aisles.csv
├── departments.csv
├── order_products.csv
├── orders.csv
└── products.csv

## Installation

**1. Create a virtual environment** (recommended)
```bash
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

## Outils utilisés



## Tools

- **pandas** — manipulation et analyse des données
- **numpy** — calcul numérique
- **matplotlib** / **seaborn** — visualisations statiques
- **plotly** — visualisations interactives
- **jupyter** — environnement du notebook

Voir `docs/methodology.md` pour une justification détaillée de chaque choix de package.

## Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) — description de chaque champ des datasets
- [`docs/methodology.md`](docs/methodology.md) — méthodologie de nettoyage, fusion et segmentation

## Équipe



