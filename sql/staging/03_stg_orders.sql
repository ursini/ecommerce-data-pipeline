CREATE TABLE IF NOT EXISTS ecommerce.stg_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date TIMESTAMP,
    status VARCHAR(30)
);