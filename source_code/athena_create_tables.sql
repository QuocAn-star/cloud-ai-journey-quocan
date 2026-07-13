-- ==========================================
-- Create External Tables (Simulation)
-- ==========================================

CREATE EXTERNAL TABLE dashboard_summary (
    total_orders BIGINT,
    total_customers BIGINT,
    total_revenue DOUBLE,
    avg_order_value DOUBLE,
    total_events BIGINT
)

CREATE EXTERNAL TABLE daily_revenue (
    order_date DATE,
    total_revenue DOUBLE
)

CREATE EXTERNAL TABLE event_summary (
    event_type STRING,
    total_events BIGINT
)

CREATE EXTERNAL TABLE country_revenue (
    country STRING,
    total_orders BIGINT,
    total_revenue DOUBLE,
    avg_order_value DOUBLE
)

CREATE EXTERNAL TABLE device_summary (
    device STRING,
    total_orders BIGINT,
    total_revenue DOUBLE,
    avg_order_value DOUBLE
)

CREATE EXTERNAL TABLE payment_summary (
    payment_method STRING,
    total_orders BIGINT,
    total_revenue DOUBLE,
    avg_order_value DOUBLE
)

CREATE EXTERNAL TABLE source_summary (
    source STRING,
    total_orders BIGINT,
    total_revenue DOUBLE,
    avg_order_value DOUBLE
)