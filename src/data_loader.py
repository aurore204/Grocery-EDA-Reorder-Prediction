import pandas as pd
#import pyarrow as pa
import os

# Chemins par défaut vers les données
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, "merged_orders.parquet")

#pa.set_cpu_count(2)  # Limite le nombre de threads à 2 pour éviter les problèmes de mémoire
#pa.set_io_thread_count(2)  # Limite le nombre de threads d'E/S à 2 pour éviter les problèmes de mémoire


def load_raw_data(raw_dir=RAW_DATA_DIR):

    orders = pd.read_csv(os.path.join(raw_dir, "orders.csv"))
    order_products = pd.read_csv(os.path.join(raw_dir, "order_products.csv"))
    products = pd.read_csv(os.path.join(raw_dir, "products.csv"))
    aisles = pd.read_csv(os.path.join(raw_dir, "aisles.csv"))
    departments = pd.read_csv(os.path.join(raw_dir, "departments.csv"))

    return {
        "orders": orders,
        "order_products": order_products,
        "products": products,
        "aisles": aisles,
        "departments": departments,
    }


def clean_order_products(order_products):

    return order_products.dropna()


def merge_all(data_dict):

    df = pd.merge(data_dict["order_products"], data_dict["orders"], on="order_id", how="left")
    df = pd.merge(df, data_dict["products"], on="product_id", how="left")
    df = pd.merge(df, data_dict["aisles"], on="aisle_id", how="left")
    df = pd.merge(df, data_dict["departments"], on="department_id", how="left")
    return df


def load_and_merge_data(raw_dir=RAW_DATA_DIR):

    data_dict = load_raw_data(raw_dir)
    data_dict["order_products"] = clean_order_products(data_dict["order_products"])
    df = merge_all(data_dict)
    return df


def save_processed_data(df: pd.DataFrame, path: str=PROCESSED_FILE):

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False, engine="fastparquet")
    print(f"Données sauvegardées dans {path}")


def load_processed_data(path: str=PROCESSED_FILE):

    if os.path.exists(path):
        return pd.read_parquet(path, engine="fastparquet")
    return None


def get_data(raw_dir=RAW_DATA_DIR, processed_path=PROCESSED_FILE, force_reload=False):
    if not force_reload:
        cached = load_processed_data(processed_path)
        if cached is not None:
            print("Chargement depuis le cache .parquet")
            return cached

    print("Pas de cache trouvé (ou rechargement forcé) : reconstruction depuis les CSV bruts")
    df = load_and_merge_data(raw_dir)
    save_processed_data(df, processed_path)
    return df