-- ============================================================
-- QUERY 1: Average Delivery Time by City
-- ============================================================
SELECT
    r.restaurant_city                           AS city,
    COUNT(o.order_id)                           AS total_orders,
    ROUND(AVG(o.total_delivery_duration_min), 1) AS avg_delivery_min,
    ROUND(MIN(o.total_delivery_duration_min), 1) AS min_delivery_min,
    ROUND(MAX(o.total_delivery_duration_min), 1) AS max_delivery_min
FROM fact_orders o
JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_city
ORDER BY avg_delivery_min DESC;

-- ============================================================
-- QUERY 2: Revenue Per City
-- ============================================================
SELECT
    r.restaurant_city                   AS city,
    COUNT(o.order_id)                   AS total_orders,
    ROUND(SUM(o.total_amount), 2)       AS total_revenue,
    ROUND(AVG(o.total_amount), 2)       AS avg_order_value,
    ROUND(SUM(o.discount), 2)           AS total_discounts_given
FROM fact_orders o
JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_city
ORDER BY total_revenue DESC;

-- ============================================================
-- QUERY 3: Cancellation Rate by City
-- ============================================================
SELECT
    r.restaurant_city                                                   AS city,
    COUNT(o.order_id)                                                   AS total_orders,
    SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)     AS cancelled_orders,
    ROUND(
        100.0 * SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)
        / COUNT(o.order_id), 2
    )                                                                   AS cancellation_rate_pct
FROM fact_orders o
JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_city
ORDER BY cancellation_rate_pct DESC;

-- ============================================================
-- QUERY 4: Top 10 Restaurants by Revenue
-- ============================================================
SELECT
    r.restaurant_name,
    r.restaurant_city,
    r.cuisine_type,
    r.restaurant_rating,
    COUNT(o.order_id)                   AS total_orders,
    ROUND(SUM(o.total_amount), 2)       AS total_revenue,
    ROUND(AVG(o.delivery_rating), 1)    AS avg_delivery_rating
FROM fact_orders o
JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_id
ORDER BY total_revenue DESC
LIMIT 10;

-- ============================================================
-- QUERY 5: Peak Order Hours
-- ============================================================
SELECT
    o.order_hour,
    COUNT(o.order_id)                           AS order_count,
    ROUND(AVG(o.total_amount), 2)               AS avg_order_value,
    ROUND(AVG(o.total_delivery_duration_min), 1) AS avg_delivery_min
FROM fact_orders o
WHERE o.order_status = 'Delivered'
GROUP BY o.order_hour
ORDER BY o.order_hour;

-- ============================================================
-- QUERY 6: Revenue by Payment Mode
-- ============================================================
SELECT
    o.payment_mode,
    COUNT(o.order_id)                   AS total_orders,
    ROUND(SUM(o.total_amount), 2)       AS total_revenue,
    ROUND(AVG(o.total_amount), 2)       AS avg_order_value
FROM fact_orders o
WHERE o.order_status = 'Delivered'
GROUP BY o.payment_mode
ORDER BY total_revenue DESC;

-- ============================================================
-- QUERY 7: Order Value Bucket Distribution
-- ============================================================
SELECT
    o.order_value_bucket,
    COUNT(o.order_id)                   AS order_count,
    ROUND(SUM(o.total_amount), 2)       AS total_revenue,
    ROUND(AVG(o.delivery_rating), 1)    AS avg_rating
FROM fact_orders o
WHERE o.order_status = 'Delivered'
GROUP BY o.order_value_bucket
ORDER BY order_count DESC;

-- ============================================================
-- QUERY 8: Delivery Delay Analysis
-- ============================================================
SELECT
    o.delivery_delay_flag,
    COUNT(o.order_id)                           AS order_count,
    ROUND(AVG(o.total_delivery_duration_min), 1) AS avg_total_time,
    ROUND(AVG(o.delivery_rating), 1)             AS avg_rating,
    ROUND(AVG(o.delivery_distance_km), 1)        AS avg_distance_km
FROM fact_orders o
WHERE o.order_status = 'Delivered'
GROUP BY o.delivery_delay_flag;

-- ============================================================
-- QUERY 9: Day-of-Week Order Patterns
-- ============================================================
SELECT
    o.order_day_of_week,
    COUNT(o.order_id)                   AS order_count,
    ROUND(SUM(o.total_amount), 2)       AS total_revenue,
    ROUND(AVG(o.total_amount), 2)       AS avg_order_value
FROM fact_orders o
WHERE o.order_status = 'Delivered'
GROUP BY o.order_day_of_week
ORDER BY order_count DESC;

-- ============================================================
-- QUERY 10: Top Cuisines by Order Volume
-- ============================================================
SELECT
    r.cuisine_type,
    COUNT(o.order_id)                           AS order_count,
    ROUND(SUM(o.total_amount), 2)               AS total_revenue,
    ROUND(AVG(o.total_delivery_duration_min), 1) AS avg_delivery_min,
    ROUND(AVG(o.delivery_rating), 1)             AS avg_rating
FROM fact_orders o
JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.cuisine_type
ORDER BY order_count DESC;
