CREATE INDEX IF NOT EXISTS idx_orders_customer_id
ON ecommerce.orders(customer_id);


CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON ecommerce.orders(order_date);


CREATE INDEX IF NOT EXISTS idx_orders_status
ON ecommerce.orders(status);


CREATE INDEX IF NOT EXISTS idx_order_items_order_id
ON ecommerce.order_items(order_id);


CREATE INDEX IF NOT EXISTS idx_order_items_product_id
ON ecommerce.order_items(product_id);