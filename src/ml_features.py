"""
Feature engineering pour la prédiction de réachat.

Construit 3 niveaux de features :
    - User       : profil d'achat global du client
    - Product    : popularité et comportement du produit
    - User×Prod  : relation spécifique entre un client et un produit

Usage:
from src.ml_features import build_all_features
user_feat, prod_feat, up_feat = build_all_features(df)

Toutes les fonctions prennent un DataFrame ligne-produit
(une ligne = un produit dans une commande) et retournent
un DataFrame agrégé au niveau indiqué.
"""

import pandas as pd
import numpy as np

def build_user_features(df: pd.DataFrame) -> pd.DataFrame:
    """Profil d'achat global par utilisateur

    Features construites :
        u_total_orders         : nombre total de commandes
        u_avg_cart_size        : taille moyenne du panier
        u_avg_days_between     : intervalle moyen entre commandes (jours)
        u_reorder_rate         : taux de réachat personnel global
        u_unique_products      : nombre de produits distincts commandés
        u_unique_departments   : diversité en départements
        u_unique_aisles        : diversité en rayons
        u_avg_unique_per_order : produits distincts par commande (moyenne)
    """
    agg = df.groupby("user_id").agg(
        u_total_orders=("order_number", "max"),
        u_avg_days_between=("days_since_prior_order", "mean"),
        u_reorder_rate=("reordered", "mean"),
        u_unique_products=("product_id", "nunique"),
        u_unique_departments=("department_id", "nunique"),
        u_unique_aisles=("aisle_id", "nunique"),
    ).reset_index()
    
    # Taille moyenne du panier
    cart_sizes = df.groupby(["user_id", "order_id"])["product_id"].count()
    avg_cart = cart_sizes.groupby("user_id").mean().reset_index(name="u_avg_cart_size")
    agg = agg.merge(avg_cart, on="user_id", how="left")
    
    # Diversité par commande
    unique_per_order = df.groupby(["user_id", "order_id"])["product_id"].nunique()
    avg_unique = unique_per_order.groupby("user_id").mean().reset_index(
        name="u_avg_unique_per_order"
    )
    agg = agg.merge(avg_unique, on="user_id", how="left")

    return agg

def build_product_features(df: pd.DataFrame) -> pd.DataFrame:
    """Popularité et comportement global par produit.

    Features construites :
        p_total_orders      : nombre de commandes contenant ce produit
        p_total_units       : nombre total d'unités vendues
        p_reorder_rate      : taux de réachat global du produit
        p_unique_users      : nombre d'acheteurs uniques
        p_avg_cart_position : position moyenne dans le panier
        p_is_organic        : flag bio (1/0)
    """
    agg = df.groupby("product_id").agg(
        p_total_orders=("order_id", "nunique"),
        p_total_units=("product_id", "count"),
        p_reorder_rate=("reordered", "mean"),
        p_unique_users=("user_id", "nunique"),
        p_avg_cart_position=("add_to_cart_order", "mean"),
    ).reset_index()

    # Flag organic
    organic = df.drop_duplicates("product_id")[["product_id", "product_name"]].copy()
    organic["p_is_organic"] = organic["product_name"].str.contains(
        r"\borganic\b", case=False, na=False
    ).astype(int)

    agg = agg.merge(organic[["product_id", "p_is_organic"]], on="product_id", how="left")
    return agg


def build_user_product_features(df: pd.DataFrame) -> pd.DataFrame:
    """Relation spécifique entre un utilisateur et un produit.

    Features construites :
        up_nb_orders         : fois où ce user a commandé ce produit
        up_reorder_rate      : taux de réachat de ce user pour ce produit
        up_avg_cart_position : position moyenne de ce produit dans le panier du user
        up_last_order_number : dernière commande contenant ce produit
        up_order_ratio       : % des commandes du user contenant ce produit
        up_orders_since_last : commandes écoulées depuis le dernier achat
    """
    up = df.groupby(["user_id", "product_id"]).agg(
        up_nb_orders=("order_id", "nunique"),
        up_reorder_rate=("reordered", "mean"),
        up_avg_cart_position=("add_to_cart_order", "mean"),
        up_last_order_number=("order_number", "max"),
    ).reset_index()

    # Ratio de commandes contenant ce produit
    user_total = df.groupby("user_id")["order_id"].nunique().reset_index(
        name="_u_total_distinct_orders"
    )
    up = up.merge(user_total, on="user_id", how="left")
    up["up_order_ratio"] = up["up_nb_orders"] / up["_u_total_distinct_orders"]

    # Commandes écoulées depuis le dernier achat de ce produit
    user_max = df.groupby("user_id")["order_number"].max().reset_index(
        name="_u_max_order_number"
    )
    up = up.merge(user_max, on="user_id", how="left")
    up["up_orders_since_last"] = up["_u_max_order_number"] - up["up_last_order_number"]

    # Nettoyage des colonnes temporaires
    up = up.drop(columns=["_u_total_distinct_orders", "_u_max_order_number"])
    return up

def build_all_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Construit les 3 niveaux de features.

    Params
    df : pd.DataFrame
        Données ligne-produit (une ligne = un produit dans une commande).
        Colonnes requises : user_id, product_id, order_id, order_number,
        reordered, add_to_cart_order, days_since_prior_order, department_id,
        aisle_id, product_name.

    Returns
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        (user_features, product_features, user_product_features)
    """
    print("  [1/3] Features utilisateur...")
    user_feat = build_user_features(df)
    print(f"  {user_feat.shape[1] - 1} features, {len(user_feat):,} users")

    print("  [2/3] Features produit...")
    prod_feat = build_product_features(df)
    print(f"  {prod_feat.shape[1] - 1} features, {len(prod_feat):,} produits")

    print("  [3/3] Features user × produit...")
    up_feat = build_user_product_features(df)
    print(f"  {up_feat.shape[1] - 2} features, {len(up_feat):,} paires")

    return user_feat, prod_feat, up_feat