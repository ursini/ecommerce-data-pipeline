SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    COUNT(DISTINCT oi.product_id) AS total_products_sold,
    COALESCE(
        SUM(oi.quantity),
        0
    ) AS total_units_sold,
    COALESCE(
        SUM(oi.quantity * oi.unit_price),
        0
    ) AS total_revenue,
    COALESCE(
        AVG(order_totals.order_total),
        0
    ) AS average_order_value
FROM ecommerce.orders AS o
INNER JOIN ecommerce.order_items AS oi
    ON o.order_id = oi.order_id
CROSS JOIN (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS order_total
    FROM ecommerce.order_items
    GROUP BY order_id
) AS order_totals
WHERE o.order_id = order_totals.order_id;