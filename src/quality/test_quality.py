import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def run_data_quality_tests():
    print("Iniciando bateria de testes de Data Quality...")
    engine = create_engine(DATABASE_URL)
    failures = []

    tests = [
        (
            "Valores nulos em chaves primárias (dim_customers)",
            "SELECT COUNT(*) FROM analytics.dim_customers WHERE customer_id IS NULL;",
        ),
        (
            "Valores nulos em chaves primárias (dim_products)",
            "SELECT COUNT(*) FROM analytics.dim_products WHERE product_id IS NULL;",
        ),
        (
            "Valores nulos em fct_sales (order_id ou item_id)",
            "SELECT COUNT(*) FROM analytics.fct_sales WHERE order_id IS NULL OR order_item_id IS NULL;",
        ),
        (
            "Preços ou valores negativos em fct_sales",
            "SELECT COUNT(*) FROM analytics.fct_sales WHERE total_amount < 0 OR unit_price < 0 OR quantity <= 0;",
        ),
        (
            "Integridade referencial de clientes em fct_sales",
            """
            SELECT COUNT(*) 
            FROM analytics.fct_sales f
            LEFT JOIN analytics.dim_customers c ON f.customer_id = c.customer_id
            WHERE c.customer_id IS NULL;
            """,
        ),
        (
            "Integridade referencial de produtos em fct_sales",
            """
            SELECT COUNT(*) 
            FROM analytics.fct_sales f
            LEFT JOIN analytics.dim_products p ON f.product_id = p.product_id
            WHERE p.product_id IS NULL;
            """,
        ),
    ]

    with engine.connect() as conn:
        for description, query in tests:
            result = conn.execute(text(query)).scalar()
            if result == 0:
                print(f"  [PASS] {description}")
            else:
                print(f"  [FAIL] {description} -> {result} registros inválidos!")
                failures.append((description, result))

    if failures:
        print(f"\n❌ Falha em {len(failures)} teste(s) de integridade.")
        sys.exit(1)
    else:
        print("\n✔ Todos os testes de Data Quality passaram com sucesso!")


if __name__ == "__main__":
    run_data_quality_tests()