"""
features.py  est un fichier contenant des fonctions réutilisables pour le projet JOJA.

Ajoute des colonnes dérivées au DataFrame fusionné pour alimenter les analyses des catégories.

    1. Rayon / Département
    2. Porduits
    3. Comportement d'achat
    4. Temporalité

Principe: chaque fonction prend un DataFrame =, retourne un DataFrame enrichi.
enrichi_dataframe() les appelle toutes en une passe.
"""

import pandas as pd
import numpy as np

# 1. SEGMENTATION CLIENT

def add_customer_segment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Segmente les clients selon leur nombre total de commandes.

    Seuils basés sur les quartiles observés (Q1= 6, Q3 =20) :
        - occasionnel: =< 6 commandes
        - typique : 7 à 20 commandes
        - fidèles: > 20 commandes

    Utilisés par : Evolution comportement d'achat (Q1, Q2, Q3)
    """
    max_orders = df.groupby("user_id")["order_number"].max()
    max_orders.name = "user_total_orders"

    df = df.merge(max_orders, on="user_id", how="left")

    conditions = [
        df["user_total_orders"] <= 6,
        df["user_total_orders"] <= 20,
        df["user_total_orders"] > 20,
    ]
    labels = ["occasionnel", "typique", "fidèle"]
    df["customer_segment"] = np.select(conditions, labels, default="inconnu")

    df["customer_segment"] = pd.Categorical(
        df["customer_segment"],
        categories=["occasionnel", "typique", "fidèle"],
        ordered=True,
    )
    return df

# 2. TAILLE DU PANIER

def add_cart_size(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nombre de produits dans chaque commande.

    Utilisé par: Produits (articles moyens par commandes),
                Rayon/Département (diversité du panier)
    """
    cart_sizes = df.groupby("order_id")["product_id"].count()
    cart_sizes.name = "cart_size"
    df = df.merge(cart_sizes, on="order_id", how="left")
    return df

# 3. DIVERSITE DU PANIER (DEPARTEMENT / AISLE)

def add_basket_diversity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nombre de départements et de rayons distincts par commande.

    Utilisé par : Rayon/Département
     - "Dans un panier, combien de départements différents ?"
     - Lien diversité - volume de commandes
    """
    dept_div = df.groupby("order_id")["department_id"].nunique()
    dept_div.name = "dept_per_order"

    aisle_div = df.groupby("order_id")["aisle_id"].nunique()
    aisle_div.name = "aisles_per_order"

    df = df.merge(dept_div, on="order_id", how="left")
    df = df.merge(aisle_div, on="order_id", how="left")
    return df

# 4. TEMPORALITE : NOMS DE JOURS ET CRENEAUX

def add_day_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converti order_dow (0=dimanche) en nom de jour lisible.

    Utilisé par : Temporalité (heatmap jour x heure),
                Produits (jour où un produit est le plus acheté)
    """
    day_map = {
        0: "Dimanche", 1: "Lundi", 2: "Mardi", 3: "Mercredi",
        4: "Jeudi", 5: "Vendredi", 6: "Samedi",
    }
    df["day_name"] = df["order_dow"].map(day_map)

    df["day_name"] = pd.Categorical(
        df["day_name"],
        categories=["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
        ordered=True,
    )
    return df

def add_hour_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Regroupe order_hour_of_day en 4 créneaux :
     - Nuit : 0h - 5h
     - Matin: 6h - 11h
     - Après-midi: 12h - 17h
     - Soir: 18h - 23h

     Utilisé par: Temporalité (patterns horaires)
    """
    conditions = [
        df["order_hour_of_day"].between(0, 5),
        df["order_hour_of_day"].between(6, 11),
        df["order_hour_of_day"].between(12, 17),
        df["order_hour_of_day"].between(18, 23),
    ]
    labels = ["Nuit", "Matin", "Après-midi", "Soir"]
    df["hour_period"] = np.select(conditions, labels, default="Inconnu")

    df["hour_period"] = pd.Categorical(
        df["hour_period"],
        categories=["Matin", "Après-midi", "Soir", "Nuit"],
        ordered=True,
    )
    return df

# PIPELINE

def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique toutes les transformations en une passe

    Usage:
        from scr.features import enrichi_dataframe
        data = enrichi_dataframe(data)

    Colonnes ajoutées:
        - customer_segment   (str)  : occasionnel / typique / fidèle
        - user_total_orders  (int)  : nb total de commandes du client
        - cart_size          (int)  : nb de produits dans la commande
        - dept_per_order     (int)  : nb de départements distincts dans la commande
        - aisles_per_order   (int)  : nb de rayons distincts dans la commande
        - day_name           (str)  : Lundi, Mardi, ...
        - hour_period        (str)  : Matin, Après-midi, Soir, Nuit
    """

    df = add_customer_segment(df)
    df = add_cart_size(df)
    df = add_basket_diversity(df)
    df = add_day_name(df)
    df = add_hour_period(df)
    return df