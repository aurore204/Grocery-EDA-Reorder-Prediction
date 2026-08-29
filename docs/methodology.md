# Méthodologie

## Choix techniques

| Outil | Rôle | Justification |
|---|---|---|
| pandas / numpy | Manipulation et calcul sur les données tabulaires | Standard de référence pour la data science en Python |
| matplotlib / seaborn | Visualisations statiques | Rendu fiable partout (GitHub, export HTML, PDF), contrairement à Plotly qui nécessite du JavaScript |
| plotly | Visualisations interactives complémentaires | Utile pour les graphiques avec de nombreuses catégories (ex: treemap), visibles dans l'export HTML |
| scipy.stats | Tests statistiques (corrélation de Pearson) | Librairie de référence pour les calculs statistiques en Python |
| scikit-learn / LightGBM | Modèles de machine learning | Standard de l'industrie pour la prédiction sur données tabulaires |

## Nettoyage des données

- Suppression d'une ligne corrompue dans `order_products (valeurs manquantes sur plusieurs colonnes simultanément, 1 seule ligne sur 10,7 millions)
- Les valeurs manquantes de `days_since_prior_order` sont conservées telles quelles : elles correspondent systématiquement à la première commande de chaque utilisateur (vérifié empiriquement, 100% de correspondance)
- Deux catégories techniques ("missing", "other") ont été identifiées parmi les rayons/départements via une vérification systématique (une seule catégorie de rayon par département, contre plusieurs pour les vrais départements). Elles sont conservées dans l'analyse (les produits eux-mêmes restent fiables), mais signalées visuellement dans les graphiques concernés.

## Segmentation client

Les clients sont répartis en 3 segments selon leur nombre total de commandes, basé sur les quartiles observés dans les données (et non un seuil arbitraire) :
- Occasionnel : ≤ 6 commandes (25% des utilisateurs)
- Typique : 7 à 20 commandes (50% des utilisateurs)
- Fidèle : > 20 commandes (25% des utilisateurs)

## Architecture du code

- `src/data_loader.py` : chargement et fusion des 5 datasets bruts, avec mise en cache au format `.parquet` pour accélérer les chargements suivants
- `src/features.py` : feature engineering partagé entre les sections (segmentation client, diversité de panier, temporalité)
- `src/ml_features.py` / `src/ml_pipeline.py` : pipeline de construction de features et d'entraînement pour la prédiction de réachat

## Approche de visualisation

Chaque graphique interactif (Plotly) est doublé d'une version statique (matplotlib/seaborn), car GitHub n'affiche pas correctement le JavaScript nécessaire aux graphiques Plotly dans son aperçu de notebook. La version interactive reste pleinement fonctionnelle dans l'export HTML du notebook final.