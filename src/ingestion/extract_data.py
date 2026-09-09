from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def extract_data():
    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    products = pd.read_csv(RAW_DATA_DIR / "products.csv")
    orders = pd.read_csv(RAW_DATA_DIR / "orders.csv")
    order_items = pd.read_csv(RAW_DATA_DIR / "order_items.csv")

    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
    }