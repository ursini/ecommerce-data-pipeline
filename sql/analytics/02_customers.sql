SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.state,
    c.country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(
        SUM(oi.quantity * oi.unit_price),
        0
    ) AS total_spent,
    COALESCE(
        AVG(oi.quantity * oi.unit_price),
        0
    ) AS average_item_value,
    MAX(o.order_date) AS last_order_date
FROM ecommerce.customers AS c
LEFT JOIN ecommerce.orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN ecommerce.order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.state,
    c.country
ORDER BY
    total_spent DESC;