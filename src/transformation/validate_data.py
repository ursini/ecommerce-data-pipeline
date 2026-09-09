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
    