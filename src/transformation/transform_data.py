import pandas as pd


def transform_customers(customers: pd.DataFrame) -> pd.DataFrame:
    customers = customers.copy()

    customers["customer_name"] = customers["customer_name"].str.strip()
    customers["email"] = customers["email"].str.strip().str.lower()
    customers["city"] = customers["city"].str.strip()
    customers["state"] = customers["state"].str.strip()
    customers["country"] = customers["country"].str.strip()

    customers["created_at"] = pd.to_datetime(
        customers["created_at"],
        errors="coerce",
    )

    customers = customers.dropna(
        subset=[
            "customer_id",
            "customer_name",
            "email",
            "created_at",
        ]
    )

    customers = customers.drop_duplicates(
        subset=["email"],
        keep="first",
    )

    return customers


def transform_products(products: pd.DataFrame) -> pd.DataFrame:
    products = products.copy()

    products["product_name"] = products["product_name"].str.strip()
    products["category"] = products["category"].str.strip()

    products["price"] = pd.to_numeric(
        products["price"],
        errors="coerce",
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce",
    )

    products["created_at"] = pd.to_datetime(
        products["created_at"],
        errors="coerce",
    )

    products = products.dropna(
        subset=[
            "product_id",
            "product_name",
            "price",
            "stock_quantity",
        ]
    )

    return products


def transform_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce",
    )

    orders["status"] = orders["status"].str.strip().str.lower()

    orders = orders.dropna(
        subset=[
            "order_id",
            "customer_id",
            "order_date",
            "status",
        ]
    )

    return orders


def transform_order_items(order_items: pd.DataFrame) -> pd.DataFrame:
    order_items = order_items.copy()

    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"],
        errors="coerce",
    )

    order_items["unit_price"] = pd.to_numeric(
        order_items["unit_price"],
        errors="coerce",
    )

    order_items = order_items.dropna(
        subset=[
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
        ]
    )

    order_items["item_total"] = (
        order_items["quantity"] * order_items["unit_price"]
    )

    return order_items