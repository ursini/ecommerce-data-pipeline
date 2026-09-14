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
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SQL_FILE = os.path.join(BASE_DIR, "sql/analytics/build_analytics.sql")


def run_transformations():
    print("Iniciando transformações analíticas no PostgreSQL...")
    engine = create_engine(DATABASE_URL)

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_content = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql_content))

        dim_cust = conn.execute(
            text("SELECT count(*) FROM analytics.dim_customers")
        ).scalar()
        dim_prod = conn.execute(
            text("SELECT count(*) FROM analytics.dim_products")
        ).scalar()
        fct_sales = conn.execute(
            text("SELECT count(*) FROM analytics.fct_sales")
        ).scalar()

        print(f"✔ analytics.dim_customers: {dim_cust} registros.")
        print(f"✔ analytics.dim_products: {dim_prod} registros.")
        print(f"✔ analytics.fct_sales: {fct_sales} registros.")

    print("\nCamada Analytics criada com sucesso!")


if __name__ == "__main__":
    run_transformations()