# T-DAT - Grocery EDA & Reorder Prediction

### Objectif du projet

Analyse exploratoire de données (EDA) et prédiction par machine learning sur un dataset réel anonymisé de livraison de courses en ligne, contenant plus de **3 millions de commandes** et **200 000 utilisateurs**.

L'objectif est d'identifier des tendances et comportements d'achat exploitables, afin de proposer des **actions concrètes pour améliorer le business** : optimisation du catalogue, ciblage marketing, fidélisation client.

### Structure du repo

```
T-DAT/
├── README.md
├── requirements.txt
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
├── grocery_eda.ipynb                  # Notebook final livrable (EDA)
├── grocery_eda.html                   # Export HTML pour partage
│
├── notebooks/                         # Notebooks d'exploration (non livrés)
│   ├── 01_data_loading_cleaning.ipynb
│   ├── 02_merge_feature_eng.ipynb
│   ├── 03_eda_questions_1_to_6.ipynb
│   ├── 04_eda_questions_7_to_12.ipynb
│   ├── 05_business_insights.ipynb
│   ├── 06_bonus_clustering.ipynb
│   └── 07_ml_reorder_prediction.ipynb # Pipeline ML prédiction de réachat
│
├── src/                               # Fonctions utilitaires partagées
│   ├── __init__.py
│   ├── data_loader.py                 # Chargement, nettoyage, fusion des tables
│   ├── features.py                    # Feature engineering EDA
│   ├── ml_features.py                 # Feature engineering ML (user, produit, user×produit)
│   └── ml_pipeline.py                 # Pipeline ML (split, train, evaluate, compare)
│
└── docs/
    ├── data_dictionary.md             # Description de chaque champ (brut + dérivé + ML)
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
python -m venv .venv
```

Activer l'environnement :

| Système | Commande |
|---|---|
| Linux / macOS | `source .venv/bin/activate` |
| Windows | `.venv\Scripts\activate` |

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Lancer le notebook**

```bash
jupyter notebook grocery_eda.ipynb
```

Pour le notebook ML :

```bash
jupyter notebook notebooks/07_ml_reorder_prediction.ipynb
```

### Outils utilisés

| Package | Rôle | Pourquoi ce choix |
|---|---|---|
| **pandas** | Manipulation et analyse des données | Standard de facto pour la data analysis en Python, API expressive et performante |
| **numpy** | Calcul numérique | Fondation de l'écosystème scientifique Python, utilisé en interne par pandas |
| **matplotlib** | Visualisations statiques | Contrôle fin sur chaque élément graphique, référence académique |
| **seaborn** | Visualisations statistiques | Surcouche de matplotlib avec des defaults esthétiques et des graphes statistiques |
| **plotly** | Visualisations interactives | Graphiques interactifs natifs dans Jupyter, idéal pour l'exploration |
| **scipy** | Tests statistiques | Corrélation de Pearson, tests de significativité |
| **statsmodels** | Analyses statistiques avancées | Modèles de régression et diagnostics statistiques |
| **squarify** | Treemaps statiques | Visualisation proportionnelle des catégories de produits |
| **scikit-learn** | ML : modèles, métriques, preprocessing | Standard de l'industrie, API cohérente et reproductible |
| **LightGBM** | Gradient boosting | Plus rapide que XGBoost sur les gros datasets tabulaires |
| **pyarrow** | Lecture/écriture Parquet | Format colonnaire rapide et compact pour le cache des données fusionnées |
| **jupyter** | Environnement de développement | Standard pour les livrables d'analyse exploratoire |

Voir [`docs/methodology.md`](docs/methodology.md) pour une justification détaillée de chaque choix.

### Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) : description de chaque champ des datasets (bruts, dérivés EDA, dérivés ML)
- [`docs/methodology.md`](docs/methodology.md) : méthodologie de nettoyage, fusion, analyse et pipeline ML