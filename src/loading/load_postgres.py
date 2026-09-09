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