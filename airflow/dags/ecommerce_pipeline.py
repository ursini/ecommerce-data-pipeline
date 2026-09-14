from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data_engineers",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="Pipeline E2E: Lake Bronze -> Postgres Staging -> Postgres Analytics -> Quality Gate",
    schedule_interval="@daily",
    catchup=False,
    tags=["ecommerce", "lake", "analytics", "quality"],
) as dag:

    extract_bronze = BashOperator(
        task_id="extract_to_bronze_lake",
        bash_command="python -m src.ingestion.extract_data",
    )

    load_staging = BashOperator(
        task_id="load_to_staging_postgres",
        bash_command="python -m src.ingestion.load_staging",
    )

    transform_analytics = BashOperator(
        task_id="transform_to_analytics_postgres",
        bash_command="python -m src.transformation.transform_analytics",
    )

    quality_gate = BashOperator(
        task_id="run_data_quality_checks",
        bash_command="python -m src.quality.test_quality",
    )

    # Fluxo completo: extração -> carga -> transformação -> validação
    extract_bronze >> load_staging >> transform_analytics >> quality_gate