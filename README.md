# E-commerce Data Pipeline

End-to-end data engineering pipeline for processing e-commerce data, applying transformations and data quality validations, loading data into PostgreSQL, generating analytical datasets, and orchestrating the workflow with Apache Airflow.

The project is fully containerized with Docker and Docker Compose, includes automated tests and centralized logging, and is designed to provide a reproducible local data engineering environment.

---

## Architecture

    Raw CSV Data
         |
         v
    +---------------------+
    |     Extraction      |
    |       Pandas        |
    +----------+----------+
               |
               v
    +---------------------+
    |   Transformation    |
    | Cleaning & Standard |
    +----------+----------+
               |
               v
    +---------------------+
    |   Data Validation   |
    | Quality & Integrity |
    +----------+----------+
               |
               v
    +---------------------+
    |      Staging        |
    |     PostgreSQL      |
    +----------+----------+
               |
               v
    +---------------------+
    |      Warehouse      |
    |   Final Data Layer  |
    +----------+----------+
               |
               v
    +---------------------+
    |      Analytics      |
    |   SQL / KPIs / BI   |
    +---------------------+

             +
             
    +---------------------+
    |       Airflow       |
    |  DAG Orchestration  |
    +----------+----------+
               |
               v
    +---------------------+
    |       Docker        |
    | Reproducible Runtime|
    +---------------------+

---

## Tech Stack

- Python 3.14
- Pandas
- PostgreSQL 16
- SQL
- Apache Airflow 3.3
- Docker
- Docker Compose
- Pytest
- python-dotenv
- psycopg2
- Git

---

## Project Structure

    ecommerce_data_pipeline/
    |
    +-- airflow/
    |   +-- dags/
    |   |   +-- ecommerce_pipeline.py
    |   +-- requirements.txt
    |   +-- Dockerfile
    |
    +-- data/
    |   +-- raw/
    |       +-- customers.csv
    |       +-- products.csv
    |       +-- orders.csv
    |       +-- order_items.csv
    |
    +-- sql/
    |   +-- ddl/
    |   |   +-- 01_create_schema.sql
    |   |   +-- 02_create_tables.sql
    |   |   +-- 03_create_indexes.sql
    |   |
    |   +-- staging/
    |   |   +-- 01_stg_customers.sql
    |   |   +-- 02_stg_products.sql
    |   |   +-- 03_stg_orders.sql
    |   |   +-- 04_stg_order_items.sql
    |   |
    |   +-- warehouse/
    |   |   +-- 02_load_final_tables.sql
    |   |
    |   +-- analytics/
    |       +-- 01_sales.sql
    |       +-- 02_customers.sql
    |       +-- 03_products.sql
    |       +-- 04_kpis.sql
    |
    +-- src/
    |   +-- ingestion/
    |   |   +-- extract_data.py
    |   |
    |   +-- transformation/
    |   |   +-- transform_data.py
    |   |   +-- validate_data.py
    |   |
    |   +-- loading/
    |   |   +-- load_postgres.py
    |   |
    |   +-- utils/
    |   |   +-- database.py
    |   |   +-- logger.py
    |   |
    |   +-- config.py
    |   +-- main.py
    |
    +-- tests/
    |   +-- test_analytics.py
    |   +-- test_config.py
    |   +-- test_logger.py
    |   +-- test_pipeline.py
    |
    +-- .dockerignore
    +-- .gitignore
    +-- Dockerfile
    +-- docker-compose.yml
    +-- requirements.txt
    +-- README.md

---

## Data Flow

The pipeline follows a structured ETL architecture.

### 1. Extraction

Raw e-commerce datasets are read from CSV files using Pandas.

Current input datasets:

- customers.csv
- products.csv
- orders.csv
- order_items.csv

The extraction layer loads the raw datasets and prepares them for downstream processing.

### 2. Transformation

The transformation layer processes each dataset independently.

Transformations are applied to:

- customers
- products
- orders
- order items

The objective is to standardize and prepare the datasets before loading them into PostgreSQL.

### 3. Validation

Data validation occurs after transformation and before database loading.

The validation layer checks:

- empty datasets
- expected data conditions
- relationship consistency
- referential integrity
- invalid values
- business rules

The main entity relationship is:

    customers
        |
        v
      orders
        |
        v
    order_items
        |
        v
     products

### 4. Staging

Validated datasets are loaded into PostgreSQL staging tables.

The staging layer acts as an intermediate layer between raw processing and the final warehouse model.

### 5. Warehouse

The final warehouse layer stores the processed e-commerce entities:

- customers
- products
- orders
- order_items

The warehouse uses:

- primary keys
- foreign keys
- unique constraints
- NOT NULL constraints
- CHECK constraints

### 6. Analytics

The analytics layer contains SQL queries for:

- sales analysis
- customer analysis
- product analysis
- KPI generation

These analytical datasets provide the foundation for reporting and future BI dashboards.

---

## Database Design

The PostgreSQL database uses the `ecommerce` schema.

Main tables:

    ecommerce.customers
    ecommerce.products
    ecommerce.orders
    ecommerce.order_items

### Customers

    customer_id
    customer_name
    email
    city
    state
    country
    created_at

### Products

    product_id
    product_name
    category
    price
    stock_quantity
    created_at

### Orders

    order_id
    customer_id
    order_date
    status

### Order Items

    order_item_id
    order_id
    product_id
    quantity
    unit_price

### Relationships

    customers.customer_id
            |
            v
    orders.customer_id

    orders.order_id
            |
            v
    order_items.order_id

    products.product_id
            |
            v
    order_items.product_id

Indexes are created on:

- orders.customer_id
- orders.order_date
- orders.status
- order_items.order_id
- order_items.product_id

---

## Data Quality

The pipeline implements multiple layers of data quality protection.

Application-level validation includes:

- empty dataframe detection
- relationship checks
- validation of transformed datasets
- business rule validation

Database-level constraints provide an additional integrity layer:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK

Examples include:

- price >= 0
- stock_quantity >= 0
- quantity > 0
- unit_price >= 0

This creates a defense-in-depth data quality strategy where data rules are enforced both in Python and PostgreSQL.

---

## Logging

Centralized logging is implemented through:

    src/utils/logger.py

Pipeline execution is logged to:

    logs/pipeline.log

Major pipeline stages are logged explicitly:

    Starting data extraction
    Data extraction completed
    Starting data transformation
    Data transformation completed
    Starting data validation
    Data validation completed
    Starting staging load
    Staging load completed
    Starting final warehouse load
    Final warehouse load completed

Errors are captured with stack traces and stage-level context.

Examples:

    Pipeline failed during data extraction
    Pipeline failed during data transformation
    Pipeline failed during data validation
    Pipeline failed during staging load
    Pipeline failed during final warehouse load

---

## Error Handling

The main pipeline uses explicit exception handling around each major execution stage.

The strategy is:

1. Log the stage where the failure occurred.
2. Capture the complete stack trace.
3. Roll back database transactions when required.
4. Re-raise exceptions.
5. Allow the orchestrator or caller to detect the failed execution.

This allows failures to be detected correctly both during local execution and inside Airflow.

---

## Configuration Management

Application configuration is centralized in:

    src/config.py

Environment variables are loaded using `python-dotenv`.

Main configuration variable:

    DATABASE_URL

Example:

    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/postgres

For Docker Compose, the application communicates with PostgreSQL through the Compose service name rather than localhost.

Environment files containing credentials are intentionally excluded from Git.

---

## Testing

The project uses Pytest for automated testing.

Test coverage includes:

### Analytics

- expected analytical columns
- row counts
- KPI structure
- KPI value constraints

### Configuration

- valid database configuration
- missing required environment variables

### Logging

- logger creation
- log file creation
- logger handlers

### Pipeline

- complete execution flow
- extraction
- transformation
- validation
- staging
- warehouse loading
- error propagation

Current test suite:

    38 tests

Run the full test suite:

    python -m pytest

---

## Docker

The project is containerized with Docker.

The main application image is defined in:

    Dockerfile

Build the image:

    docker build -t ecommerce-data-pipeline .

Run the container:

    docker run --rm --env-file .env.docker ecommerce-data-pipeline

The application image contains:

- application code
- SQL files
- raw data
- Python dependencies

Credentials are not embedded into the Docker image.

---

## Docker Compose

Docker Compose is used to reproduce the complete local infrastructure.

Services include:

- PostgreSQL
- Pipeline
- Airflow API Server
- Airflow Scheduler
- Airflow DAG Processor
- Airflow Triggerer

Start PostgreSQL:

    docker compose up -d postgres

Start the complete environment:

    docker compose up -d --build

Check services:

    docker compose ps

Stop the environment:

    docker compose down

---

## PostgreSQL Container

PostgreSQL 16 is used as the main relational database.

Database initialization is performed through SQL files mounted into:

    /docker-entrypoint-initdb.d/

Initialization order:

    01_create_schema.sql
          |
          v
    02_create_tables.sql
          |
          v
    03_create_indexes.sql
          |
          v
    staging table definitions

The PostgreSQL container includes a healthcheck using `pg_isready`.

The pipeline waits for PostgreSQL to become healthy before starting.

---

## Airflow

Apache Airflow 3.3 is used for workflow orchestration.

Airflow runs entirely inside Docker and does not need to be installed in the local Python virtual environment.

The DAG is located at:

    airflow/dags/ecommerce_pipeline.py

DAG ID:

    ecommerce_data_pipeline

Airflow services include:

- airflow-api-server
- airflow-scheduler
- airflow-dag-processor
- airflow-triggerer

The Airflow metadata database is separated from the ecommerce database.

### Airflow UI

The local interface is available at:

    http://localhost:8080

The local development environment uses Airflow's `SimpleAuthManager`.

Airflow is responsible for orchestration, while the core data processing logic remains inside the project's Python modules.

---

## Airflow DAG

The DAG currently orchestrates the pipeline flow:

    Extract
       |
       v
    Transform
       |
       v
    Validate
       |
       v
    Load Staging
       |
       v
    Load Warehouse

The core Python logic remains reusable outside Airflow.

The same business logic can therefore be executed:

- directly with Python
- inside Docker
- through Docker Compose
- through Airflow

---

## Local Development

### Create a virtual environment

    python -m venv .venv

Activate on Windows:

    .venv\Scripts\activate

### Install dependencies

    pip install -r requirements.txt

### Configure environment variables

Create a local `.env` file:

    POSTGRES_PASSWORD=your_password
    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/postgres

### Run the pipeline

    python -m src.main

### Run tests

    python -m pytest

---

## Running the Complete Environment

Start the complete stack:

    docker compose up -d --build

Verify services:

    docker compose ps

Open Airflow:

    http://localhost:8080

Run the pipeline through:

    ecommerce_data_pipeline

---

## Reproducibility

The project is designed to be reproducible through:

- versioned Python code
- versioned SQL scripts
- Docker images
- Docker Compose
- environment variables
- automated tests
- Airflow DAGs

This minimizes dependency on the host machine's Python and database configuration.

The local Python environment is primarily used for development and testing, while Docker provides the reproducible runtime environment.

---

## Engineering Decisions

### Separation of Concerns

The codebase separates:

- ingestion
- transformation
- validation
- loading
- analytics
- orchestration
- configuration
- logging
- testing

This improves maintainability and makes each layer easier to test.

### Staging Layer

A staging layer separates transformed data from the final warehouse layer.

### Database Constraints

Data integrity is enforced at both the application and database levels.

### Centralized Configuration

Connection settings are centralized instead of being duplicated across the project.

### Centralized Logging

Pipeline stages produce consistent structured logs.

### Containerized Execution

Docker provides a consistent runtime environment.

### Orchestration

Airflow provides workflow orchestration and execution tracking.

---

## Current Status

The implementation currently includes:

- Raw CSV ingestion
- Data transformation
- Data validation
- PostgreSQL staging
- PostgreSQL warehouse
- SQL analytics
- Data quality rules
- Database constraints
- Database indexes
- Automated tests
- Centralized logging
- Pipeline error handling
- Docker image
- Docker Compose
- PostgreSQL container
- Airflow 3.3
- Airflow DAG
- Airflow UI
- Containerized orchestration

---

## Future Improvements

Potential next improvements include:

- split the Airflow DAG into independent tasks
- task-level retries
- task-level logging
- incremental data loading
- partitioning for larger datasets
- data lineage
- monitoring and alerting
- CI/CD with GitHub Actions
- coverage reporting
- production-oriented secrets management
- cloud deployment
- warehouse optimization
- automated data quality reporting

---

## Project Goals

The project demonstrates practical data engineering capabilities across the complete data lifecycle:

    Raw Data
       |
       v
    Ingestion
       |
       v
    Transformation
       |
       v
    Validation
       |
       v
    Staging
       |
       v
    Warehouse
       |
       v
    Analytics
       |
       v
    Orchestration

The final architecture combines Python, SQL, PostgreSQL, Docker, Docker Compose, automated testing and Apache Airflow into a reproducible end-to-end data engineering environment.

---

## Author

End-to-end data engineering project focused on building a reliable, testable, containerized and orchestrated e-commerce data pipeline.