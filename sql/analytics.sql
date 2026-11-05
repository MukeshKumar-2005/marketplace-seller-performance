
USE performance_db;

-- 1. Top 5 sellers by revenue

SELECT
    s.seller_id,
    s.seller_name,
    s.city,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_items_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue

FROM sellers s

INNER JOIN order_items oi
    ON s.seller_id = oi.seller_id

GROUP BY
    s.seller_id,
    s.seller_name,
    s.city

ORDER BY total_revenue DESC

LIMIT 5;




-- 2. Revenue by Product Category

SELECT
    p.category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_items_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue

FROM products p

INNER JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.category

ORDER BY
    total_revenue DESC;






-- 3. Monthly Revenue Trends

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS revenue_month,

    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(oi.quantity) AS total_items_sold,

    SUM(oi.quantity * oi.unit_price) AS monthly_revenue

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

GROUP BY
    DATE_FORMAT(o.order_date, '%Y-%m')

ORDER BY
    revenue_month ASC;





-- 4. Average Order Value (AOV)

SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(oi.quantity * oi.unit_price) AS total_revenue,

    ROUND(
        SUM(oi.quantity * oi.unit_price)
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id;





-- 5. Best-Selling Products

SELECT
    p.product_id,
    p.product_name,
    p.category,

    SUM(oi.quantity) AS total_quantity_sold,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    SUM(oi.quantity * oi.unit_price) AS total_revenue

FROM products p

INNER JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category

ORDER BY
    total_quantity_sold DESC

LIMIT 10;





-- 6. Seller Performance Ranking

SELECT
    s.seller_id,
    s.seller_name,
    s.city,

    sp.total_orders,
    sp.total_revenue,
    sp.average_order_value,

    RANK() OVER (
        ORDER BY sp.total_revenue DESC
    ) AS revenue_rank

FROM seller_performance sp

INNER JOIN sellers s
    ON sp.seller_id = s.seller_id

ORDER BY revenue_rank ASC;
