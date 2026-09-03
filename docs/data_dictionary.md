# Dictionnaire de données

Ce document décrit chaque champ des données brutes ainsi que les colonnes dérivées ajoutées lors du feature engineering.

## Données brutes

### Table `products`

| Champ | Description |
|---|---|
| product_id | Identifiant unique du produit |
| product_name | Nom du produit |
| aisle_id | Identifiant du rayon auquel appartient le produit |
| department_id | Identifiant du département auquel appartient le produit |

### Table `aisles`

| Champ | Description |
|---|---|
| aisle_id | Identifiant unique du rayon |
| aisle | Nom du rayon |

### Table `departments`

| Champ | Description |
|---|---|
| department_id | Identifiant unique du département |
| department | Nom du département |

### Table `orders`

| Champ | Description |
|---|---|
| order_id | Identifiant unique de la commande |
| user_id | Identifiant unique de l'utilisateur |
| eval_set | Catégorie technique du dataset source |
| order_number | Numéro de séquence de la commande pour cet utilisateur (1 = première commande) |
| order_dow | Jour de la semaine de la commande (0 = dimanche) |
| order_hour_of_day | Heure de la commande (0-23) |
| days_since_prior_order | Nombre de jours depuis la commande précédente (vide pour la première commande de chaque utilisateur) |

### Table `order_products`

| Champ | Description |
|---|---|
| order_id | Identifiant de la commande |
| product_id | Identifiant du produit |
| add_to_cart_order | Position du produit dans le panier (1 = ajouté en premier) |
| reordered | 1 si le produit a déjà été commandé avant par cet utilisateur, 0 sinon |

## Colonnes dérivées — EDA (voir `src/features.py`)

| Champ | Description |
|---|---|
| customer_segment | Segment client : occasionnel (≤6 commandes) / typique (7-20) / fidèle (>20) |
| user_total_orders | Nombre total de commandes de l'utilisateur |
| cart_size | Nombre de produits dans la commande |
| dept_per_order | Nombre de départements distincts dans la commande |
| aisles_per_order | Nombre de rayons distincts dans la commande |
| day_name | Nom du jour de la semaine (dérivé de `order_dow`) |
| hour_period | Créneau horaire : Matin / Après-midi / Soir / Nuit |

## Colonnes dérivées — ML (voir `src/ml_features.py`)

### Features utilisateur (`u_*`)

Calculées au niveau de chaque utilisateur sur l'ensemble de son historique (hors dernière commande pour le train set).

| Champ | Description |
|---|---|
| u_total_orders | Nombre total de commandes passées |
| u_avg_cart_size | Taille moyenne du panier (nombre de produits par commande) |
| u_avg_days_between | Intervalle moyen entre deux commandes (en jours) |
| u_reorder_rate | Taux de réachat personnel global (proportion de produits réachetés) |
| u_unique_products | Nombre de produits distincts commandés au total |
| u_unique_departments | Nombre de départements distincts fréquentés |
| u_unique_aisles | Nombre de rayons distincts fréquentés |

### Features produit (`p_*`)

Calculées au niveau de chaque produit sur l'ensemble des commandes.

| Champ | Description |
|---|---|
| p_total_orders | Nombre de commandes contenant ce produit |
| p_reorder_rate | Taux de réachat global du produit (tous utilisateurs confondus) |
| p_unique_users | Nombre d'acheteurs uniques de ce produit |
| p_avg_cart_position | Position moyenne du produit dans le panier |
| p_is_organic | Flag bio : 1 si le nom contient "organic", 0 sinon |

### Features user × produit (`up_*`)

Calculées pour chaque paire (utilisateur, produit), elles capturent la relation spécifique entre un client et un produit donné. Ce sont les features les plus prédictives du modèle (~91 % de l'importance).

| Champ | Description |
|---|---|
| up_nb_orders | Nombre de fois où cet utilisateur a commandé ce produit |
| up_reorder_rate | Taux de réachat de cet utilisateur pour ce produit spécifique |
| up_avg_cart_position | Position moyenne de ce produit dans le panier de cet utilisateur |
| up_last_order_number | Numéro de la dernière commande contenant ce produit |
| up_order_ratio | Proportion des commandes de l'utilisateur contenant ce produit |
| up_orders_since_last | Nombre de commandes passées depuis le dernier achat de ce produit |

## Points d'attention

- Deux catégories techniques ("missing" et "other") existent parmi les rayons/départements : elles regroupent des produits dont la catégorisation d'origine n'était pas renseignée dans les données sources. Voir l'analyse détaillée dans la section Rayon/Département du notebook.
- Le fichier `order_products.csv` ne couvre qu'un sous-ensemble des commandes de `orders.csv` (environ 1 million sur 3,4 millions, soit 92,1% des utilisateurs représentés avec une partie de leur historique de commandes). Les `order_id` présents dans ce fichier se suivent presque sans interruption (de 2 à environ 1 133 485), ce qui indique un sous-ensemble continu des commandes. La raison exacte de cette troncature n'est pas connue avec certitude — voir l'investigation détaillée dans `01_data_loading_cleaning.ipynb`.
- Les features ML sont calculées **uniquement sur le train set** (toutes les commandes sauf la dernière de chaque utilisateur) pour éviter le data leakage. Les paires user×produit absentes du train sont remplies à 0 (l'utilisateur n'a jamais acheté ce produit, ce qui est une information en soi).