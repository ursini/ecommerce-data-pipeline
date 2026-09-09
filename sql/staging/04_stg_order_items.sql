CREATE TABLE IF NOT EXISTS ecommerce.stg_order_items (
    order_item_id BIGINT,
    order_id BIGINT,
    product_id BIGINT,
    quantity INTEGER,
    unit_price NUMERIC(12, 2)
);