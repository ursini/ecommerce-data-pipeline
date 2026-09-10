SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.customer_id,
    c.customer_name,
    p.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS item_total
FROM ecommerce.orders AS o
INNER JOIN ecommerce.customers AS c
    ON o.customer_id = c.customer_id
INNER JOIN ecommerce.order_items AS oi
    ON o.order_id = oi.order_id
INNER JOIN ecommerce.products AS p
    ON oi.product_id = p.product_id
ORDER BY
    o.order_date,
    o.order_id,
    oi.order_item_id;