from pathlib import Path

from src.utils.database import get_connection


BASE_DIR = Path(__file__).resolve().parents[1]
ANALYTICS_DIR = BASE_DIR / "sql" / "analytics"


def execute_query(file_name: str):
    sql_file = ANALYTICS_DIR / file_name
    sql = sql_file.read_text(encoding="utf-8")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return columns, rows

    finally:
        conn.close()


def test_sales_analytics_returns_expected_columns():
    columns, rows = execute_query("01_sales.sql")

    expected_columns = {
        "order_id",
        "order_date",
        "status",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "item_total",
    }

    assert expected_columns.issubset(set(columns))
    assert len(rows) == 16


def test_customer_analytics_returns_one_row_per_customer():
    columns, rows = execute_query("02_customers.sql")

    expected_columns = {
        "customer_id",
        "customer_name",
        "email",
        "total_orders",
        "total_spent",
        "average_item_value",
        "last_order_date",
    }

    assert expected_columns.issubset(set(columns))
    assert len(rows) == 5


def test_product_analytics_returns_one_row_per_product():
    columns, rows = execute_query("03_products.sql")

    expected_columns = {
        "product_id",
        "product_name",
        "category",
        "price",
        "stock_quantity",
        "total_orders",
        "units_sold",
        "total_revenue",
    }

    assert expected_columns.issubset(set(columns))
    assert len(rows) == 8


def test_kpi_analytics_returns_single_row():
    columns, rows = execute_query("04_kpis.sql")

    expected_columns = {
        "total_orders",
        "total_customers",
        "total_products_sold",
        "total_units_sold",
        "total_revenue",
        "average_order_value",
    }

    assert expected_columns.issubset(set(columns))
    assert len(rows) == 1


def test_kpi_values_are_not_negative():
    _, rows = execute_query("04_kpis.sql")

    result = rows[0]

    assert result[0] >= 0
    assert result[1] >= 0
    assert result[2] >= 0
    assert result[3] >= 0
    assert result[4] >= 0
    assert result[5] >= 0