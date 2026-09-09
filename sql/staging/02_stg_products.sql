CREATE TABLE IF NOT EXISTS ecommerce.stg_products (
    product_id BIGINT,
    product_name VARCHAR(200),
    category VARCHAR(100),
    price NUMERIC(12, 2),
    stock_quantity INTEGER,
    created_at TIMESTAMP
);