---
title: "Step 4: Amazon Athena"
date: 2024-01-01
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

# Step 4: Amazon Athena Queries

In this step, you will configure Amazon Athena to query the Gold-tier tables registered in the Glue Data Catalog, verify the pipeline results, and explore the data with business queries.

**Estimated time:** 15–20 minutes

---

## Prerequisites

- Step 3 complete (Glue ETL jobs ran successfully, 7 tables in Glue Catalog)
- S3 `athena-results/` prefix exists

---

## 4.1 Configure Athena Query Result Location

**AWS Console → Amazon Athena → Query editor → Settings → Manage**

| Field | Value |
|-------|-------|
| Query result location | `s3://customer-behavior-lakehouse1/athena-results/` |
| Encryption | SSE-S3 |

Click **Save**.

> ⚠️ **Important:** Athena cannot run queries until a result location is configured. This step is mandatory.

**CLI alternative:**
```bash
aws athena update-work-group \
    --work-group primary \
    --configuration-updates '{
        "ResultConfigurationUpdates": {
            "OutputLocation": "s3://customer-behavior-lakehouse1/athena-results/"
        }
    }'
```

---

## 4.2 Configure Athena Workgroup (FinOps Best Practice)

Create a dedicated Workgroup with per-query cost controls:

**AWS Console → Athena → Administration → Workgroups → Create workgroup**

| Field | Value |
|-------|-------|
| Workgroup name | `lakehouse-wg` |
| Query result location | `s3://customer-behavior-lakehouse1/athena-results/` |
| Encrypt query results | ✅ SSE-S3 |
| Override client-side settings | ✅ Enabled |
| **Data usage controls** | |
| - Per-query limit | 1 GB |
| - Action if query exceeds limit | Cancel query |

Click **Create workgroup**.

> 💡 **FinOps note:** The 1 GB per-query scan limit acts as a safety net - any runaway query that would scan too much data is automatically cancelled before incurring excessive cost. At $5/TB, 1 GB = $0.005 maximum per query.

---

## 4.3 Select the Database in Query Editor

In the Athena Query Editor:
- **Data source**: `AwsDataCatalog`
- **Database**: `customer_behavior_catalog_db`
- **Workgroup**: `lakehouse-wg`

You should see 7 tables in the left panel:
- `dashboard_summary`
- `daily_revenue`
- `event_summary`
- `country_revenue`
- `device_summary`
- `payment_summary`
- `source_summary`

---

## 4.4 Create External Tables (Manual Fallback)

If the Glue ETL Job 3 did not auto-register tables (or for manual verification), run the `CREATE TABLE` statements from `athena_create_tables.sql`:

```sql
-- Dashboard Summary table
CREATE EXTERNAL TABLE IF NOT EXISTS dashboard_summary (
    total_orders    BIGINT,
    total_customers BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE,
    total_events    BIGINT
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/dashboard_summary/';

-- Daily Revenue table
CREATE EXTERNAL TABLE IF NOT EXISTS daily_revenue (
    order_date    DATE,
    total_revenue DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/daily_revenue/';

-- Event Summary table
CREATE EXTERNAL TABLE IF NOT EXISTS event_summary (
    event_type   STRING,
    total_events BIGINT
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/event_summary/';

-- Country Revenue table
CREATE EXTERNAL TABLE IF NOT EXISTS country_revenue (
    country         STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/country_revenue/';

-- Device Summary table
CREATE EXTERNAL TABLE IF NOT EXISTS device_summary (
    device          STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/device_summary/';

-- Payment Summary table
CREATE EXTERNAL TABLE IF NOT EXISTS payment_summary (
    payment_method  STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/payment_summary/';

-- Source Summary table
CREATE EXTERNAL TABLE IF NOT EXISTS source_summary (
    source          STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/source_summary/';
```

---

## 4.5 Run Business Queries & Validate Results

Execute the following queries from `athena_queries.sql` to verify the pipeline results:

### Query 1: Overall Dashboard Metrics

```sql
SELECT * FROM dashboard_summary;
```

**Expected result:** 1 row with total orders, customers, revenue, average order value, and total events.

![Athena - Dashboard Summary query result](/result/Athenas/Dashboard%20Summary.jpg)

---

### Query 2: Daily Revenue Trend

```sql
SELECT *
FROM daily_revenue
ORDER BY order_date;
```

**Expected result:** ~365 rows, one per day, showing daily revenue totals.

![Athena - Daily Revenue query in editor](/result/Athenas/daily%20revenue.jpg)

![Athena - Daily Revenue result data](/result/Athenas/result_daily_revenue.jpg)

---

### Query 3: Event Frequency

```sql
SELECT *
FROM event_summary
ORDER BY total_events DESC;
```

**Expected result:** 5–8 rows showing event types (page_view, add_to_cart, purchase, checkout, etc.) sorted by frequency.

![Athena - Event Summary query result](/result/Athenas/Event%20Summary.jpg)

---

### Query 4: Revenue by Country

```sql
SELECT *
FROM country_revenue
ORDER BY total_revenue DESC
LIMIT 10;
```

**Expected result:** Countries sorted by total revenue - e.g., US, UK, DE, FR, JP, VN, SG.

---

### Query 5: Revenue by Payment Method

```sql
SELECT *
FROM payment_summary
ORDER BY total_revenue DESC;
```

**Expected result:** 3 rows: credit_card, paypal, bank_transfer.

---

### Query 6: Revenue by Device Type

```sql
SELECT *
FROM device_summary
ORDER BY total_revenue DESC;
```

**Expected result:** 3 rows: mobile, desktop, tablet.

---

### Query 7: Revenue by Traffic Source

```sql
SELECT *
FROM source_summary
ORDER BY total_revenue DESC;
```

**Expected result:** 4 rows: organic, social, email, paid_ads.

---

## 4.6 Check Metrics & Cost

After running queries, verify performance metrics:

**Data scanned per query:**

In Athena Query Editor, after each query completes, look at the **Data scanned** metric shown below the results. With Parquet format on compact Gold tables:
- `dashboard_summary` → ~5–20 KB scanned
- `daily_revenue` → ~10–50 KB scanned
- `country_revenue` → ~5–20 KB scanned

This is extremely efficient compared to scanning raw CSV (which would scan 1–10 MB per query).

**Check CloudWatch metrics for Athena via CLI:**
```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/Athena \
    --metric-name DataScannedInBytes \
    --dimensions Name=WorkGroup,Value=lakehouse-wg \
    --start-time $(date -u -d '1 hour ago' '+%Y-%m-%dT%H:%M:%SZ') \
    --end-time $(date -u '+%Y-%m-%dT%H:%M:%SZ') \
    --period 3600 \
    --statistics Sum
```

---

## 4.7 Test Error Scenarios

**Test 1: Query a non-existent table**
```sql
SELECT * FROM non_existent_table;
```
Expected error: `TABLE_NOT_FOUND: line 1:15: Table 'awsdatacatalog.customer_behavior_catalog_db.non_existent_table' does not exist`

**Test 2: Trigger workgroup cost limit**
```sql
-- This should fail if Silver table is registered and is large (> 1 GB)
SELECT * FROM silver_orders;
```
Expected: `Query cancelled - data usage limit exceeded` (workgroup protection working)

**Test 3: Syntax error handling**
```sql
SELECT FROM dashboard_summary;
```
Expected: `SYNTAX_ERROR: line 1:8: mismatched input 'FROM'`

---

## 4.8 Expected Results Summary

| Table | Expected Row Count | Key Business Insight |
|-------|-------------------|----------------------|
| `dashboard_summary` | 1 row | Total orders, customers, revenue, avg order value, total events |
| `daily_revenue` | ~365 rows | Revenue per day showing growth/decline trends |
| `event_summary` | ~5–8 rows | Most frequent user actions on the platform |
| `country_revenue` | ~7–10 rows | Which geography drives the most revenue |
| `device_summary` | 3 rows | Mobile vs desktop vs tablet revenue split |
| `payment_summary` | 3 rows | Credit card vs PayPal vs bank transfer preference |
| `source_summary` | 4 rows | Organic vs paid vs social vs email effectiveness |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `HIVE_METASTORE_ERROR: Database not found` | Wrong database selected in Query Editor | Select `customer_behavior_catalog_db` in the dropdown |
| `No output location provided` | Query result location not configured | Complete Step 4.1 - set result location |
| Query returns 0 rows | Gold table is empty (Job 3 failed) | Re-run `silver-to-gold-job` and check it succeeded |
| `TABLE_NOT_FOUND` | Tables not registered by Job 3 | Run CREATE TABLE statements from Step 4.4 manually |

✅ **Step 4 complete** - Proceed to [Step 5: Deploy Streamlit Dashboard on EC2](../5.4.5-EC2-Dashboard/)
