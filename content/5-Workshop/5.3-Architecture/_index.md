---
title: "Architecture Description"
date: 2024-01-01
weight: 3
chapter: false
pre: " <b> 5.3 </b> "
---

# Architecture Description

## Overall Architecture

The platform implements a **Serverless Medallion Data Lakehouse** pattern - data flows through four S3 tiers (Raw → Bronze → Silver → Gold), processed by AWS Glue ETL jobs, queried by Amazon Athena, and visualized on a Streamlit Dashboard hosted on EC2 within a VPC.

---

## Layer-by-Layer Description

### Layer 1: VPC & Networking

The entire platform runs within an **Amazon VPC** to ensure network isolation and security.

```
VPC: 10.0.0.0/16
 └── Public Subnet: 10.0.1.0/24 (us-east-1a)
      └── EC2 Instance (Streamlit Dashboard)
           └── Elastic IP (static public IP)
 └── Internet Gateway → attached to VPC
 └── Route Table → 0.0.0.0/0 → Internet Gateway
 └── Security Group (EC2):
      Inbound: port 22 (SSH), port 8501 (Streamlit)
      Outbound: all traffic
```

**Why VPC?** Running EC2 inside a VPC ensures the dashboard cannot be accessed from arbitrary internet sources. The Security Group acts as a stateful firewall - only explicitly allowed ports (22 for SSH management, 8501 for Streamlit) are open.

![VPC Dashboard - Your VPCs](/result/VPC/Your%20VPCs..jpg)

![Subnets created inside VPC](/result/VPC/Subnets.jpg)

![Internet Gateway attached to VPC](/result/VPC/Internet%20Gateway.jpg)

![Route Tables - 0.0.0.0/0 route to IGW](/result/VPC/Route%20Tables.jpg)

![Security Group - inbound rules for port 22 and 8501](/result/VPC/Security%20Group.jpg)

---

### Layer 2: S3 Data Lake - Medallion Architecture

Four prefixes within one S3 bucket form the data lake tiers:

```
s3://customer-behavior-lakehouse1/
├── raw/                          ← Original source data (CSV + streaming JSON)
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── order_items.csv
│   ├── reviews.csv
│   ├── sessions.csv
│   └── streaming/events/2026/07/06/08/   ← Firehose delivered JSON
│
├── bronze/                       ← Converted to Parquet, no transformation
│   ├── customers/
│   ├── orders/
│   ├── products/
│   ├── order_items/
│   ├── reviews/
│   ├── sessions/
│   └── events/
│
├── silver/                       ← Cleansed, deduplicated, schema-normalized
│   └── [same table structure as bronze]
│
├── gold/                         ← Business KPI aggregations (registered in Glue Catalog)
│   ├── event_summary/
│   ├── daily_revenue/
│   ├── payment_summary/
│   ├── country_revenue/
│   ├── device_summary/
│   ├── source_summary/
│   └── dashboard_summary/
│
└── athena-results/               ← Athena query result storage
```

**Raw tier** - original data as-is from source systems (CSV files and Firehose JSON):

![S3 Raw - original source data](/result/S3/S3%20Raw%20-%20d%E1%BB%AF%20li%E1%BB%87u%20g%E1%BB%91c.jpg)

**Firehose streaming data** delivered to Raw/streaming/:

![Firehose streaming data delivered to S3](/result/S3/FirehoseStreaming%20%C4%91%C3%A3%20%C4%91%E1%BB%95%20data%20v%C3%A0o%20S3.jpg)

**Bronze tier** - Parquet format, schema preserved from Raw:

![S3 Bronze - Parquet converted data](/result/S3/S3%20Bronze.jpg)

**Silver tier** - clean, deduplicated, normalized data:

![S3 Silver - cleansed data](/result/S3/S3%20Silver.jpg)

**Gold tier** - business KPI aggregations ready for Athena:

![S3 Gold - KPI aggregation data](/result/S3/S3%20Gold.jpg)

---

### Layer 3: Ingestion Layer

**Streaming Path (Firehose → S3 Raw):**
- Amazon API Gateway receives HTTP POST events from clients
- Events are proxied to Amazon Data Firehose
- Firehose buffers events (60 seconds or 1 MB) and delivers to `s3://.../raw/streaming/`
- A Lambda function can be attached to Firehose for inline transformation

**Batch Path (Lambda → S3 Raw):**
- Amazon EventBridge Scheduler fires on a cron schedule
- Triggers a Lambda function that reads the source database
- Lambda extracts records and writes CSV to `s3://.../raw/`

---

### Layer 4: Processing Layer - AWS Glue ETL

Three sequential Glue ETL jobs process data through the Medallion tiers:

**Job 1: `raw_to_bronze_job.py` - Raw → Bronze**

Reads CSV files from S3 Raw, converts to Parquet, and writes to Bronze. Also reads streaming JSON events from the Firehose-delivered path.

```python
BUCKET_NAME = "customer-behavior-lakehouse1"
RAW_PATH = f"s3://{BUCKET_NAME}/raw/"
BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"

# Process each CSV table
csv_tables = ["customers", "orders", "products", "order_items", "reviews", "sessions"]
for table in csv_tables:
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{RAW_PATH}{table}.csv")
    df.write.mode("overwrite").parquet(f"{BRONZE_PATH}{table}/")

# Process Firehose streaming events (JSON)
events_df = spark.read.option("recursiveFileLookup", "true").json(
    f"s3://{BUCKET_NAME}/raw/streaming/events/2026/07/06/08/"
)
events_df.write.mode("overwrite").parquet(f"{BRONZE_PATH}events/")
```

**Job 2: `bronze_to_silver_job.py` - Bronze → Silver**

Applies data quality transformations:
- `dropDuplicates()` - removes exact duplicate rows
- Column name normalization (lowercase, underscores)
- String trimming for all StringType columns
- Timestamp parsing for date/time columns

```python
for table in tables:
    df = spark.read.parquet(f"{BRONZE_PATH}{table}/")
    df = df.dropDuplicates()
    # Normalize column names: strip, lowercase, replace spaces/hyphens with underscore
    for old_col in df.columns:
        new_col = old_col.strip().lower().replace(" ", "_").replace("-", "_")
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)
    # Trim string columns
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, trim(col(field.name)))
    # Parse timestamps
    for column_name in df.columns:
        if any(kw in column_name.lower() for kw in ["date", "time", "timestamp"]):
            df = df.withColumn(column_name, to_timestamp(col(column_name)))
    df.write.mode("overwrite").parquet(f"{SILVER_PATH}{table}/")
```

**Job 3: `silver_to_gold_job.py` - Silver → Gold**

Computes business KPI aggregations and **registers results in the Glue Data Catalog** automatically:

| Gold Table | Source | Description |
|------------|--------|-------------|
| `event_summary` | events | Count of events by type |
| `daily_revenue` | orders | Total revenue per day |
| `payment_summary` | orders | Orders + revenue by payment method |
| `country_revenue` | orders | Orders + revenue by country |
| `device_summary` | orders | Orders + revenue by device type |
| `source_summary` | orders | Orders + revenue by traffic source |
| `dashboard_summary` | orders + events | Overall totals (orders, customers, revenue, events) |

After Job 3 runs, these tables are automatically available in Athena without any manual crawlers.

![AWS Glue - ETL Jobs list showing all 3 jobs](/result/AWS%20Glue/AWS%20Glue%20Jobs.jpg)

![Glue Data Catalog Database - customer_behavior_catalog_db](/result/AWS%20Glue/Glue%20Database.jpg)

![Glue Catalog Tables - all 7 Gold tables registered](/result/AWS%20Glue/Glue%20Tables.jpg)

---

### Layer 5: Query Layer - Amazon Athena

Amazon Athena reads Gold-tier tables registered in the Glue Data Catalog and executes SQL queries serverlessly - no infrastructure to provision.

```sql
-- Overall dashboard metrics
SELECT * FROM dashboard_summary;

-- Daily revenue trend
SELECT * FROM daily_revenue ORDER BY order_date;

-- Top countries by revenue
SELECT * FROM country_revenue ORDER BY total_revenue DESC;

-- Event frequency
SELECT * FROM event_summary ORDER BY total_events DESC;
```

**FinOps advantage:** Athena charges $5 per TB scanned. Gold tables in Parquet format are compact (typically 10–100 KB per table for workshop data), making each query cost fractions of a cent.

![Athena - Dashboard Summary query result](/result/Athenas/Dashboard%20Summary.jpg)

![Athena - Daily Revenue query result](/result/Athenas/daily%20revenue.jpg)

![Athena - Event Summary query result](/result/Athenas/Event%20Summary.jpg)

---

### Layer 6: Visualization Layer - Streamlit Dashboard on EC2

The Streamlit application (`app_beautiful.py`) runs on an EC2 instance and queries Athena via `awswrangler`:

```python
import awswrangler as wr
import boto3

DATABASE = "customer_behavior_catalog_db"
ATHENA_OUTPUT = "s3://customer-behavior-lakehouse1/athena-results/"

@st.cache_data(ttl=600)
def load_table(table_name: str):
    return wr.athena.read_sql_query(
        sql=f"SELECT * FROM {table_name}",
        database=DATABASE,
        s3_output=ATHENA_OUTPUT,
        boto3_session=boto3.Session(region_name="us-east-1")
    )
```

The dashboard displays 8 interactive charts + KPI cards covering all business dimensions.

![EC2 Instance running the Streamlit dashboard](/result/EC2/EC2%20Instance.jpg)

![EC2 Security Group - ports 22 and 8501 open](/result/EC2/Security%20Group.jpg)

**Dashboard screenshots:**

![Revenue Trend - daily revenue over time](/result/DashBoard/Revenue%20Trend.png)

![Top 10 Countries by Revenue](/result/DashBoard/Top%2010%20Countries%20by%20Revenue.png)

![Revenue by Device type](/result/DashBoard/Revenue%20by%20Device.png)

![Revenue by Payment Method](/result/DashBoard/Revenue%20by%20Payment%20Method.png)

![Revenue by Traffic Source](/result/DashBoard/Revenue%20by%20Traffic%20Source.png)

![Event Distribution by type](/result/DashBoard/Event%20Distribution.png)

![Top Performers summary table](/result/DashBoard/Top%20Performers.jpg)

![View Daily Revenue Data - expandable table](/result/DashBoard/View%20Daily%20Revenue%20Data.jpg)

---

## Service Selection Rationale

| Service | Why Selected | Alternative Considered |
|---------|-------------|------------------------|
| **Amazon S3** | Cheapest durable object storage; pay per GB stored; no minimum; perfect for data lake | EFS (too expensive), EBS (not shared) |
| **AWS Glue** | Fully managed PySpark; pay per DPU-second; no cluster to provision | EMR (requires cluster management, higher cost) |
| **Amazon Athena** | Pay per TB scanned; Parquet reduces scans 85%; no warehouse provisioning | Redshift ($700+/month for smallest cluster) |
| **Amazon Data Firehose** | Zero capacity planning; built-in buffering; natively writes to S3 | Kinesis Data Streams (requires shard management) |
| **AWS Lambda** | Pay per 100ms invocation; zero idle cost; perfect for event-driven transforms | EC2 worker (always-on cost) |
| **Amazon EC2 (t3.micro)** | Free Tier eligible; sufficient for Streamlit web app | Fargate/App Runner (slightly more complex) |
| **EventBridge Scheduler** | Serverless cron; 14M free invocations/month | EC2 cron (requires always-on instance) |
| **Glue Data Catalog** | Free up to 1M objects; unified metadata for Athena; no separate metastore | Glue Crawlers with schedule (costs DPU-hours per crawl) |

---

## Data Flow Summary

```
[Website/Mobile Events]
         │  HTTP POST
         ▼
   API Gateway ──► Firehose ──► Lambda (optional transform)
                                       │  JSON (batched)
                                       ▼
                              s3://lakehouse/raw/streaming/
                                       
[E-commerce DB]
         │  Schedule (EventBridge)
         ▼
      Lambda ──► s3://lakehouse/raw/ (CSV files)
                        │
                        ▼
              AWS Glue Job 1 (Raw → Bronze)
              CSV/JSON → Parquet, schema inferred
                        │
                        ▼
              AWS Glue Job 2 (Bronze → Silver)
              dropDuplicates + normalize + trim + timestamps
                        │
                        ▼
              AWS Glue Job 3 (Silver → Gold)
              7 KPI aggregations + auto Catalog registration
                        │
                        ▼
               Glue Data Catalog
               (7 external tables pointing to Gold S3)
                        │
                        ▼
              Amazon Athena (serverless SQL)
                        │
                        ▼
       Streamlit Dashboard (EC2 in VPC)
       awswrangler → Athena → results to browser
```

✅ **Architecture understood** - Proceed to [Step-by-Step Hands-On](../5.4-Steps/)
