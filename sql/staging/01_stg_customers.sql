CREATE TABLE IF NOT EXISTS ecommerce.stg_customers (
    customer_id BIGINT,
    customer_name VARCHAR(150),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP
);