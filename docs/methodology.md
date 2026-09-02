# Méthodologie

## Choix techniques

| Outil | Rôle | Justification |
|---|---|---|
| pandas / numpy | Manipulation et calcul sur les données tabulaires | Standard de référence pour la data science en Python |
| matplotlib / seaborn | Visualisations statiques | Rendu fiable partout (GitHub, export HTML, PDF), contrairement à Plotly qui nécessite du JavaScript |
| plotly | Visualisations interactives complémentaires | Utile pour les graphiques avec de nombreuses catégories (ex: treemap), visibles dans l'export HTML |
| scipy.stats | Tests statistiques (corrélation de Pearson) | Librairie de référence pour les calculs statistiques en Python |
| statsmodels | Analyses statistiques complémentaires | Tests de significativité et modèles statistiques avancés |
| squarify | Treemaps statiques | Visualisation proportionnelle des catégories de produits |
| scikit-learn | Logistic Regression, Random Forest, métriques, preprocessing | Standard de l'industrie pour le ML en Python, API cohérente et reproductible |
| LightGBM | Gradient boosting | Plus rapide que XGBoost sur les gros datasets tabulaires, gère nativement les valeurs manquantes |
| pyarrow | Lecture/écriture au format Parquet | Format colonnaire rapide et compact pour le cache des données fusionnées |

## Nettoyage des données

- Suppression d'une ligne corrompue dans `order_products` (valeurs manquantes sur plusieurs colonnes simultanément, 1 seule ligne sur 10,7 millions)
- Les valeurs manquantes de `days_since_prior_order` sont conservées telles quelles : elles correspondent systématiquement à la première commande de chaque utilisateur (vérifié empiriquement, 100% de correspondance)
- Deux catégories techniques ("missing", "other") ont été identifiées parmi les rayons/départements via une vérification systématique (une seule catégorie de rayon par département, contre plusieurs pour les vrais départements). Elles sont conservées dans l'analyse (les produits eux-mêmes restent fiables), mais signalées visuellement dans les graphiques concernés.

## Segmentation client

Les clients sont répartis en 3 segments selon leur nombre total de commandes, basé sur les quartiles observés dans les données (et non un seuil arbitraire) :
- Occasionnel : ≤ 6 commandes (25% des utilisateurs)
- Typique : 7 à 20 commandes (50% des utilisateurs)
- Fidèle : > 20 commandes (25% des utilisateurs)

## Architecture du code

- `src/data_loader.py` : chargement et fusion des 5 datasets bruts, avec mise en cache au format `.parquet` pour accélérer les chargements suivants
- `src/features.py` : feature engineering partagé entre les sections EDA (segmentation client, diversité de panier, temporalité) et fonction réutilisable `reorder_rate_by_group` pour les analyses croisées
- `src/ml_features.py` : construction des features ML à 3 niveaux (utilisateur, produit, user×produit)
- `src/ml_pipeline.py` : pipeline complet de split, assemblage, entraînement et évaluation des modèles

## Approche de visualisation

Chaque graphique interactif (Plotly) est doublé d'une version statique (matplotlib/seaborn), car GitHub n'affiche pas correctement le JavaScript nécessaire aux graphiques Plotly dans son aperçu de notebook. La version interactive reste pleinement fonctionnelle dans l'export HTML du notebook final.

Une palette personnalisée cohérente est utilisée dans l'ensemble du notebook :
- Bleu clair (`#a8c4d9`) → clients occasionnels
- Bleu moyen (`#4a7fa5`) → clients typiques
- Bleu marine (`#1b3a4b`) → clients fidèles
- Terracotta (`#c45c3c`) → accent pour les éléments à mettre en avant

## Pipeline ML — Prédiction de réachat

### Problème

Prédire si un produit donné sera réacheté (`reordered = 1`) dans la prochaine commande d'un utilisateur. C'est un problème de classification binaire.

### Split temporel

On utilise un split temporel et non un split aléatoire, pour éviter le data leakage :
- **Train** : toutes les commandes de chaque utilisateur sauf la dernière
- **Test** : la dernière commande de chaque utilisateur

Ce choix reflète le cas d'usage réel : prédire la prochaine commande à partir de l'historique passé. Le ratio résultant (~93 % train / ~7 % test) est un résultat naturel de cette approche, pas un choix arbitraire.

### Feature engineering

Les features sont calculées uniquement sur le train set et organisées en 3 niveaux :
- **Utilisateur** (7 features) : profil global du client (fréquence, diversité, taux de réachat personnel)
- **Produit** (5 features) : popularité du produit (volume, taux de réachat global, flag bio)
- **User × Produit** (6 features) : relation spécifique entre un client et un produit (nombre d'achats, régularité, récence)

Voir `docs/data_dictionary.md` pour la description détaillée de chaque feature.

### Modèles comparés

| Modèle | Type | Rôle dans la comparaison |
|---|---|---|
| Logistic Regression | Linéaire | Baseline interprétable — établit un plancher de performance |
| Random Forest | Ensemble (bagging) | Capture les interactions non-linéaires entre features |
| LightGBM | Ensemble (boosting) | État de l'art sur données tabulaires, rapide sur gros volumes |

La Logistic Regression est enveloppée dans un `StandardScaler` car les features ont des échelles très différentes (de 0-1 pour les ratios à plusieurs milliers pour les compteurs). Les modèles à base d'arbres (Random Forest, LightGBM) n'ont pas besoin de scaling — les arbres de décision sont insensibles à l'échelle des variables.

### Métriques d'évaluation

| Métrique | Ce qu'elle mesure |
|---|---|
| Accuracy | Proportion de prédictions correctes sur l'ensemble |
| Precision | Fiabilité des prédictions positives ("quand le modèle dit réacheté, a-t-il raison ?") |
| Recall | Couverture des vrais positifs ("combien de réachats réels sont détectés ?") |
| F1-score | Moyenne harmonique precision/recall — métrique principale de comparaison |
| ROC-AUC | Capacité du modèle à classer correctement les probabilités |

## Démarche d'analyse
 
Pour chaque question, une hypothèse de départ est formulée avant l'exploration des données, puis confrontée aux résultats obtenus. Cette approche permet de vérifier si l'intuition initiale est confirmée, infirmée, ou seulement partiellement correcte.
 
## Gestion des classements avec égalités multiples
 
Certaines analyses impliquent des centaines de valeurs à égalité (ex: produits commandés une seule fois), rendant un simple "top N" peu fiable. Dans ces cas, les valeurs sont regroupées par tranches (`pd.cut`) plutôt que classées individuellement.
 
## Diversité des visualisations
 
Un même type de graphique n'est jamais réutilisé pour des besoins différents (comparaison,distribution, proportion, relation), par exemple, la section Produits combine histogramme, bar chart, bar chart groupé et heatmap selon le besoin de chaque question.