CREATE SCHEMA IF NOT EXISTS analytics;

-- 1. Dimensão Clientes
DROP TABLE IF EXISTS analytics.dim_customers CASCADE;
CREATE TABLE analytics.dim_customers AS
SELECT 
    customer_id,
    customer_name,
    email,
    city,
    state,
    country,
    CAST(created_at AS TIMESTAMP) AS created_at
FROM ecommerce.stg_customers;

-- 2. Dimensão Produtos
DROP TABLE IF EXISTS analytics.dim_products CASCADE;
CREATE TABLE analytics.dim_products AS
SELECT 
    product_id,
    product_name,
    category,
    CAST(price AS NUMERIC(10, 2)) AS price
FROM ecommerce.stg_products;

-- 3. Tabela Fato de Vendas
DROP TABLE IF EXISTS analytics.fct_sales CASCADE;
CREATE TABLE analytics.fct_sales AS
SELECT 
    oi.order_item_id,
    o.order_id,
    o.customer_id,
    oi.product_id,
    CAST(oi.quantity AS INT) AS quantity,
    CAST(oi.unit_price AS NUMERIC(10, 2)) AS unit_price,
    CAST(oi.quantity * oi.unit_price AS NUMERIC(10, 2)) AS total_amount,
    CAST(o.order_date AS TIMESTAMP) AS order_date,
    o.status AS order_status
FROM ecommerce.stg_orders o
JOIN ecommerce.stg_order_items oi ON o.order_id = oi.order_id;

-- 4. Índices analíticos
CREATE INDEX IF NOT EXISTS idx_fct_sales_customer ON analytics.fct_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fct_sales_product ON analytics.fct_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fct_sales_date ON analytics.fct_sales(order_date);