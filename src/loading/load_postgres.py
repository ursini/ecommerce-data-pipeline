from pathlib import Path

import pandas as pd

from src.utils.database import get_connection


BASE_DIR = Path(__file__).resolve().parents[2]


def load_customers(customers: pd.DataFrame) -> None:
    if customers.empty:
        raise ValueError("Customers dataframe is empty")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE ecommerce.stg_customers"
            )

            for row in customers.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO ecommerce.stg_customers (
                        customer_id,
                        customer_name,
                        email,
                        city,
                        state,
                        country,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row.customer_id,
                        row.customer_name,
                        row.email,
                        row.city,
                        row.state,
                        row.country,
                        row.created_at,
                    ),
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def load_products(products: pd.DataFrame) -> None:
    if products.empty:
        raise ValueError("Products dataframe is empty")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE ecommerce.stg_products"
            )

            for row in products.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO ecommerce.stg_products (
                        product_id,
                        product_name,
                        category,
                        price,
                        stock_quantity,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row.product_id,
                        row.product_name,
                        row.category,
                        row.price,
                        row.stock_quantity,
                        row.created_at,
                    ),
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def load_orders(orders: pd.DataFrame) -> None:
    if orders.empty:
        raise ValueError("Orders dataframe is empty")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE ecommerce.stg_orders"
            )

            for row in orders.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO ecommerce.stg_orders (
                        order_id,
                        customer_id,
                        order_date,
                        status
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        row.order_id,
                        row.customer_id,
                        row.order_date,
                        row.status,
                    ),
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def load_order_items(order_items: pd.DataFrame) -> None:
    if order_items.empty:
        raise ValueError("Order items dataframe is empty")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE ecommerce.stg_order_items"
            )

            for row in order_items.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO ecommerce.stg_order_items (
                        order_item_id,
                        order_id,
                        product_id,
                        quantity,
                        unit_price
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        row.order_item_id,
                        row.order_id,
                        row.product_id,
                        row.quantity,
                        row.unit_price,
                    ),
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def load_final_tables() -> None:
    sql_file = (
        BASE_DIR
        / "sql"
        / "warehouse"
        / "02_load_final_tables.sql"
    )

    if not sql_file.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_file}"
        )

    sql = sql_file.read_text(encoding="utf-8")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()