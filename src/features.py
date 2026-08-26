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
    