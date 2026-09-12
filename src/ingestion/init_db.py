import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Ordem exata de execução dos scripts DDL e Staging
SQL_SCRIPTS = [
    "sql/ddl/01_create_schema.sql",
    "sql/staging/01_stg_customers.sql",
    "sql/staging/02_stg_products.sql",
    "sql/staging/03_stg_orders.sql",
    "sql/staging/04_stg_order_items.sql",
    "sql/ddl/02_create_tables.sql",
    "sql/ddl/03_create_indexes.sql",
]


def initialize_database():
    engine = create_engine(DATABASE_URL)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    print("Inicializando schemas e tabelas no PostgreSQL...\n")

    with engine.begin() as conn:
        for script_rel_path in SQL_SCRIPTS:
            full_path = os.path.join(base_dir, script_rel_path)
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    sql_content = f.read().strip()
                    if sql_content:
                        conn.execute(text(sql_content))
                        print(f"✔ Executado com sucesso: {script_rel_path}")
            else:
                print(f"⚠ Arquivo ignorado (não encontrado): {script_rel_path}")

    print("\nBanco de dados estruturado com sucesso!")


if __name__ == "__main__":
    initialize_database()