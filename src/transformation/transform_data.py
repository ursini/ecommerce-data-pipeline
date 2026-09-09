import pandas as pd


def transform_customers(customers: pd.DataFrame) -> pd.DataFrame:
    customers = customers.copy()

    # Padroniza campos de texto
    customers["customer_name"] = customers["customer_name"].str.strip()
    customers["email"] = customers["email"].str.strip().str.lower()
    customers["city"] = customers["city"].str.strip()
    customers["state"] = customers["state"].str.strip()
    customers["country"] = customers["country"].str.strip()

    # Converte data para datetime
    customers["created_at"] = pd.to_datetime(customers["created_at"])

    # Remove registros sem campos obrigatórios
    customers = customers.dropna(
        subset=["customer_id", "customer_name", "email"]
    )

    # Remove clientes duplicados pelo e-mail
    customers = customers.drop_duplicates(
        subset=["email"],
        keep="first"
    )

    return customers