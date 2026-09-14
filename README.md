[![Continuous Integration](https://github.com/ursini/ecommerce-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/ursini/ecommerce-data-pipeline/actions/workflows/ci.yml)

# E-commerce Data Pipeline

End-to-end data engineering platform designed to extract, process, validate, model, and orchestrate e-commerce transaction data. The project implements a multi-hop architecture (Data Lake Bronze -> Relational Staging -> Dimensional Analytics Star Schema), applies an automated Data Quality gate, serves business KPIs via Metabase BI, and orchestrates workflows using Apache Airflow.

The entire platform is containerized with Docker and Docker Compose, features continuous integration via GitHub Actions, automated tests with Pytest, and centralized logging.

---

## Architecture

```text
    Raw CSV Sources
           |
           v
    +-----------------------+
    |  Extraction (Bronze)  |
    |    MinIO / S3 Lake    |
    +-----------+-----------+
                |
                v
    +-----------------------+
    |  Staging Layer (PostgreSQL)
    |   Schema: ecommerce   |
    +-----------+-----------+
                |
                v
    +-----------------------+
    | Dimensional Analytics |
    | Star Schema: analytics|
    | (dim_cust, dim_prod,  |
    |      fct_sales)       |
    +-----------+-----------+
                |
                v
    +-----------------------+
    |   Data Quality Gate   |
    |  Integrity, Nulls,    |
    |   Business Rules      |
    +-----------+-----------+
                |
                v
    +-----------------------+
    |   Consumption / BI    |
    |  Metabase Dashboards  |
    +-----------------------+

                +

    +-----------------------+
    |    Apache Airflow     |
    | DAG Orchestration     |
    +-----------+-----------+
                |
                v
    +-----------------------+
    | Docker & Compose      |
    | Reproducible Runtime  |
    +-----------------------+
```

---

## Pipeline Execution & Analytics

### Orchestrated Workflow (Apache Airflow)
![Airflow Pipeline](docs/images/airflow_dag.png)

### Executive BI Dashboard (Metabase)
![Metabase Dashboard](docs/images/metabase_dashboard.png)

---

## Tech Stack

- **Language:** Python 3.12+
- **Data Processing:** Pandas, SQLAlchemy, Psycopg2
- **Data Storage & DW:** PostgreSQL 16
- **Object Storage (Data Lake):** MinIO (S3-compatible)
- **Business Intelligence:** Metabase
- **Workflow Orchestration:** Apache Airflow
- **Containerization:** Docker & Docker Compose
- **Testing & Quality:** Pytest, Custom SQL Data Quality Gate
- **CI/CD:** GitHub Actions
- **Configuration & Logging:** python-dotenv, Python standard logging

---

## Project Structure

```text
ecommerce_data_pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── airflow/
│   ├── dags/
│   │   └── ecommerce_pipeline.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── data/
│   └── raw/
│       ├── customers.csv
│       ├── products.csv
│       ├── orders.csv
│       └── order_items.csv
│
├── docs/
│   └── images/
│       ├── airflow_dag.png
│       └── metabase_dashboard.png
│
├── sql/
│   ├── ddl/
│   │   ├── 01_create_schema.sql
│   │   ├── 02_create_tables.sql
│   │   └── 03_create_indexes.sql
│   ├── staging/
│   │   ├── 01_stg_customers.sql
│   │   ├── 02_stg_products.sql
│   │   ├── 03_stg_orders.sql
│   │   └── 04_stg_order_items.sql
│   └── analytics/
│       └── build_analytics.sql
│
├── src/
│   ├── ingestion/
│   │   ├── extract_data.py
│   │   └── load_staging.py
│   ├── transformation/
│   │   └── transform_analytics.py
│   ├── quality/
│   │   └── test_quality.py
│   ├── utils/
│   │   ├── database.py
│   │   └── logger.py
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_analytics.py
│   ├── test_config.py
│   ├── test_logger.py
│   └── test_pipeline.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Data Flow & Architecture Layers

### 1. Extraction (Bronze Layer)
Raw e-commerce datasets (`customers`, `products`, `orders`, `order_items`) are extracted, validated, and loaded into MinIO (S3-compatible object storage) in column-oriented Parquet format.

### 2. Staging Layer (PostgreSQL `ecommerce` schema)
Data from the object storage is ingested into normalized staging tables inside PostgreSQL (`stg_customers`, `stg_products`, `stg_orders`, `stg_order_items`). Types are cast, and initial database constraints are enforced.

### 3. Analytics Layer (PostgreSQL `analytics` schema)
Transformations convert staging data into an analytical **Star Schema** designed for efficient OLAP querying:
- **`analytics.dim_customers`:** Customer attributes, geographical information, and account creation dates.
- **`analytics.dim_products`:** Product catalog, categories, and unit list prices.
- **`analytics.fct_sales`:** Granular sales transactions at the item level. Aggregates quantity, unit price, total amount, and links foreign keys to customer and product dimensions with optimized b-tree indexes.

### 4. Data Quality Gate
Before exposing datasets to downstream consumers, the pipeline triggers an automated Data Quality verification script (`src/quality/test_quality.py`):
- Non-null primary key checks for dimensions and fact tables.
- Numerical validity checks (no negative prices, revenue, or non-positive quantities).
- Referential integrity verification to prevent orphan records between fact and dimension tables.
- Fails fast by throwing non-zero exit codes to block corrupted runs in Airflow.

### 5. Consumption & BI (Metabase)
Metabase connects directly to PostgreSQL's `analytics` schema, rendering executive dashboards with key business metrics:
- **Total GMV (Gross Merchandise Value)**
- **Average Order Value (AOV)**
- **Order Volume by Status**
- **Sales Trend Analysis over time**

---

## Airflow Orchestration

The end-to-end execution is scheduled and managed using **Apache Airflow**.

The DAG (`airflow/dags/ecommerce_pipeline.py`) enforces strict task dependencies and automated retries:

```text
extract_to_bronze_lake >> load_to_staging_postgres >> transform_to_analytics_postgres >> run_data_quality_checks
```

- **DAG ID:** `ecommerce_pipeline`
- **Schedule:** `@daily`
- **Retries:** 1 retry with a 2-minute delay upon failure.

---

## Local Development & Setup

### 1. Clone the Repository & Configure Environment
```bash
git clone [https://github.com/ursini/ecommerce-data-pipeline](https://github.com/ursini/ecommerce-data-pipeline).