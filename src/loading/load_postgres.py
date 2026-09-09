import pandas as pd

from src.utils.database import get_connection


def load_customers(customers: pd.DataFrame) -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
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



def load_orders(orders: pd.DataFrame) -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
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
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
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