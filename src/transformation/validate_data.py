import pandas as pd


def validate_customers(customers: pd.DataFrame) -> None:
    required_columns = [
        "customer_id",
        "customer_name",
        "email",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in customers.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if customers["customer_id"].isna().any():
        raise ValueError("customer_id contains null values")

    if customers["email"].isna().any():
        raise ValueError("email contains null values")

    if customers["email"].duplicated().any():
        raise ValueError("Duplicate customer emails found")


def validate_products(products: pd.DataFrame) -> None:
    required_columns = [
        "product_id",
        "product_name",
        "price",
        "stock_quantity",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in products.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if products["product_id"].isna().any():
        raise ValueError("product_id contains null values")

    if products["product_name"].isna().any():
        raise ValueError("product_name contains null values")

    if (products["price"] < 0).any():
        raise ValueError("Negative product prices found")

    if (products["stock_quantity"] < 0).any():
        raise ValueError("Negative stock quantities found")

    if products["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs found")
    