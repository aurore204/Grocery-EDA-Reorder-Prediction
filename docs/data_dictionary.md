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

## Colonnes dérivées (voir `src/features.py`)

| Champ | Description |
|---|---|
| customer_segment | Segment client : occasionnel (≤6 commandes) / typique (7-20) / fidèle (>20) |
| user_total_orders | Nombre total de commandes de l'utilisateur |
| cart_size | Nombre de produits dans la commande |
| dept_per_order | Nombre de départements distincts dans la commande |
| aisles_per_order | Nombre de rayons distincts dans la commande |
| day_name | Nom du jour de la semaine (dérivé de `order_dow`) |
| hour_period | Créneau horaire : Matin / Après-midi / Soir / Nuit |

## Points d'attention

- Deux catégories techniques ("missing" et "other") existent parmi les rayons/départements : elles regroupent des produits dont la catégorisation d'origine n'était pas renseignée dans les données sources. Voir l'analyse détaillée dans la section Rayon/Département du notebook.
- Le fichier `order_products.csv` ne couvre qu'un sous-ensemble des commandes de `orders.csv` (environ 1 million sur 3,4 millions) une 
  troncature volontaire du fichier source pour en réduire la taille.