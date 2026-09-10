TRUNCATE TABLE
    ecommerce.order_items,
    ecommerce.orders,
    ecommerce.products,
    ecommerce.customers;


INSERT INTO ecommerce.customers (
    customer_id,
    customer_name,
    email,
    city,
    state,
    country,
    created_at
)
SELECT
    customer_id,
    customer_name,
    email,
    city,
    state,
    country,
    created_at
FROM ecommerce.stg_customers;


INSERT INTO ecommerce.products (
    product_id,
    product_name,
    category,
    price,
    stock_quantity,
    created_at
)
SELECT
    product_id,
    product_name,
    category,
    price,
    stock_quantity,
    created_at
FROM ecommerce.stg_products;


INSERT INTO ecommerce.orders (
    order_id,
    customer_id,
    order_date,
    status
)
SELECT
    order_id,
    customer_id,
    order_date,
    status
FROM ecommerce.stg_orders;


INSERT INTO ecommerce.order_items (
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price
)
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price
FROM ecommerce.stg_order_items;