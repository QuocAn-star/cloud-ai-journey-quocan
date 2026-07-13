-- Dashboard Summary
SELECT *
FROM dashboard_summary

-- Daily Revenue
SELECT *
FROM daily_revenue
ORDER BY order_date

-- Event Summary
SELECT *
FROM event_summary
ORDER BY total_events DESC

-- Revenue by Country
SELECT *
FROM country_revenue
ORDER BY total_revenue DESC

-- Revenue by Device
SELECT *
FROM device_summary
ORDER BY total_revenue DESC

-- Revenue by Payment Method
SELECT *
FROM payment_summary
ORDER BY total_revenue DESC

-- Revenue by Traffic Source
SELECT *
FROM source_summary
ORDER BY total_revenue DESC