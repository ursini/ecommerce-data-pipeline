import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.ingestion.extract_data import extract_data
from src.transformation.transform_data import transform_customers
from src.transformation.validate_data import (
    validate_customers,
    validate_products,
    validate_orders,
    validate_order_items,
)

from src.loading.load_postgres import (
    load_customers,
    load_products,
    load_orders,
    load_order_items,
)



data = extract_data()

data["customers"] = transform_customers(data["customers"])

validate_customers(data["customers"])
validate_products(data["products"])
validate_orders(data["orders"])
validate_order_items(data["order_items"])

for name, df in data.items():
    print(f"{name}: {df.shape}")