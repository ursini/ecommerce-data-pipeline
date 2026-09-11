FROM apache/airflow:3.3.0

COPY airflow/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV PYTHONPATH=/opt/airflow

COPY airflow/dags /opt/airflow/dags
COPY src /opt/airflow/src
COPY data /opt/airflow/data
COPY sql /opt/airflow/sql