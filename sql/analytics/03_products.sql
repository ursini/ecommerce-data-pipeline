SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.stock_quantity,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COALESCE(
        SUM(oi.quantity),
        0
    ) AS units_sold,
    COALESCE(
        SUM(oi.quantity * oi.unit_price),
        0
    ) AS total_revenue
FROM ecommerce.products AS p
LEFT JOIN ecommerce.order_items AS oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.stock_quantity
ORDER BY
    total_revenue DESC;