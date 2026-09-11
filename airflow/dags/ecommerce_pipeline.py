from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from src.ingestion.extract_data import extract_data

from src.transformation.transform_data import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items,
)

from src.transformation.validate_data import (
    validate_customers,
    validate_products,
    validate_orders,
    validate_order_items,
    validate_relationships,
)

from src.loading.load_postgres import (
    load_customers,
    load_products,
    load_orders,
    load_order_items,
    load_final_tables,
)


def run_pipeline():
    data = extract_data()

    data["customers"] = transform_customers(data["customers"])
    data["products"] = transform_products(data["products"])
    data["orders"] = transform_orders(data["orders"])
    data["order_items"] = transform_order_items(data["order_items"])

    validate_customers(data["customers"])
    validate_products(data["products"])
    validate_orders(data["orders"])
    validate_order_items(data["order_items"])

    validate_relationships(
        data["customers"],
        data["products"],
        data["orders"],
        data["order_items"],
    )

    load_customers(data["customers"])
    load_products(data["products"])
    load_orders(data["orders"])
    load_order_items(data["order_items"])
    load_final_tables()


with DAG(
    dag_id="ecommerce_data_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "etl"],
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_ecommerce_pipeline",
        python_callable=run_pipeline,
    )