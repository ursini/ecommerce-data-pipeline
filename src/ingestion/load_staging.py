import io
import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Conexão MinIO
S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
BUCKET_BRONZE = "lake-bronze"

# Conexão Postgres
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TABLE_MAPPING = {
    "customers.parquet": "stg_customers",
    "products.parquet": "stg_products",
    "orders.parquet": "stg_orders",
    "order_items.parquet": "stg_order_items",
}


def load_bronze_to_staging():
    s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadminpassword",
    )
    engine = create_engine(DATABASE_URL)

    print("Iniciando carga do Data Lake para o PostgreSQL...")

    with engine.begin() as conn:
        # 1. Garante que o schema staging exista ANTES de tentar criar as tabelas
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))

        # 2. Faz a leitura e inserção
        for file_name, table_name in TABLE_MAPPING.items():
            response = s3.get_object(Bucket=BUCKET_BRONZE, Key=file_name)
            df = pd.read_parquet(io.BytesIO(response["Body"].read()))

            df.to_sql(
                name=table_name,
                con=conn,
                schema="staging",
                if_exists="replace",
                index=False,
            )
            print(f"✔ staging.{table_name} carregada com sucesso ({len(df)} linhas).")

    print("\nCarga finalizada com 100% de sucesso!")


if __name__ == "__main__":
    load_bronze_to_staging()