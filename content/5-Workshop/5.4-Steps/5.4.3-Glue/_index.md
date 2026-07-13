---
title: "Step 3: AWS Glue ETL"
date: 2024-01-01
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

# Step 3: AWS Glue ETL Jobs

In this step, you will create the Glue Data Catalog database and three ETL jobs that process data through the Medallion tiers: **Raw → Bronze → Silver → Gold**.

**Estimated time:** 30–40 minutes

> ⚠️ **Order matters:** Always run Job 1 before Job 2, and Job 2 before Job 3. Each job reads from the previous tier's output.

---

## Prerequisites

- Step 2 complete (S3 bucket with Raw data and scripts uploaded)
- IAM role `AWSGlueServiceRole-lakehouse` created (Step 2.5)

---

## 3.1 Create Glue Data Catalog Database

**AWS Console → AWS Glue → Data Catalog → Databases → Add database**

| Field | Value |
|-------|-------|
| Database name | `customer_behavior_catalog_db` |
| Description | `Catalog for Customer Behavior Lakehouse Gold tables` |
| Location (optional) | `s3://customer-behavior-lakehouse1/gold/` |

Click **Create database**.

**CLI alternative:**
```bash
aws glue create-database \
    --database-input '{
        "Name": "customer_behavior_catalog_db",
        "Description": "Catalog for Customer Behavior Lakehouse Gold tables",
        "LocationUri": "s3://customer-behavior-lakehouse1/gold/"
    }'
```

![Glue Data Catalog Database - customer_behavior_catalog_db created](/result/AWS%20Glue/Glue%20Database.jpg)

---

## 3.2 Create Glue ETL Job 1: Raw → Bronze

**AWS Console → AWS Glue → ETL Jobs → Create job → Script editor (Spark)**

Select **Spark** as the engine. Paste the full content of `raw_to_bronze_job.py` into the editor.

**Job properties:**

| Field | Value |
|-------|-------|
| Name | `raw-to-bronze-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Language | Python 3 |
| Worker type | G.1X |
| Number of workers | 2 |
| Job timeout | 30 minutes |
| Script path | `s3://customer-behavior-lakehouse1/scripts/raw_to_bronze_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**What this job does (`raw_to_bronze_job.py`):**

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

BUCKET_NAME = "customer-behavior-lakehouse1"
RAW_PATH = f"s3://{BUCKET_NAME}/raw/"
BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"

# === Process 6 CSV tables ===
csv_tables = ["customers", "orders", "products", "order_items", "reviews", "sessions"]

for table in csv_tables:
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(f"{RAW_PATH}{table}.csv")
    )
    df.write.mode("overwrite").parquet(f"{BRONZE_PATH}{table}/")
    print(f"Saved Bronze: {table}")

# === Process Firehose streaming events ===
events_path = f"s3://{BUCKET_NAME}/raw/streaming/events/2026/07/06/08/"
events_df = spark.read.option("recursiveFileLookup", "true").json(events_path)
events_df.write.mode("overwrite").parquet(f"{BRONZE_PATH}events/")

print("Raw → Bronze completed successfully.")
job.commit()
```

Click **Save** then **Run**.

**Monitor the job:**
- Go to **Runs** tab
- Wait for status to change from `Running` → `Succeeded` (~3–5 minutes)

**Validate Bronze output:**
```bash
aws s3 ls s3://customer-behavior-lakehouse1/bronze/ --recursive | head -20
```

Expected: Parquet part files in each table subdirectory under `bronze/`.

![S3 Bronze - Parquet files created from CSV data](/result/S3/S3%20Bronze.jpg)

---

## 3.3 Create Glue ETL Job 2: Bronze → Silver

**AWS Console → AWS Glue → ETL Jobs → Create job → Script editor (Spark)**

| Field | Value |
|-------|-------|
| Name | `bronze-to-silver-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Worker type | G.1X |
| Number of workers | 2 |
| Script path | `s3://customer-behavior-lakehouse1/scripts/bronze_to_silver_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**What this job does (`bronze_to_silver_job.py`):**

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, trim, to_timestamp
from pyspark.sql.types import StringType
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

BUCKET_NAME = "customer-behavior-lakehouse1"
BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"
SILVER_PATH = f"s3://{BUCKET_NAME}/silver/"

tables = ["customers", "orders", "products", "order_items", "reviews", "sessions", "events"]

def clean_column_name(name):
    return name.strip().lower().replace(" ", "_").replace("-", "_")

for table in tables:
    df = spark.read.parquet(f"{BRONZE_PATH}{table}/")

    # Step 1: Remove duplicate rows
    df = df.dropDuplicates()

    # Step 2: Normalize column names
    for old_col in df.columns:
        new_col = clean_column_name(old_col)
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)

    # Step 3: Trim whitespace from string columns
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, trim(col(field.name)))

    # Step 4: Parse timestamp columns
    for column_name in df.columns:
        lower_name = column_name.lower()
        if "date" in lower_name or "time" in lower_name or "timestamp" in lower_name:
            df = df.withColumn(column_name, to_timestamp(col(column_name)))

    df.write.mode("overwrite").parquet(f"{SILVER_PATH}{table}/")
    print(f"Written Silver: {table}")

print("Bronze to Silver job completed successfully.")
job.commit()
```

Run the job and wait for **Succeeded** status (~5–8 minutes).

**Validate Silver output:**
```bash
aws s3 ls s3://customer-behavior-lakehouse1/silver/ --recursive | head -20
```

![S3 Silver - Cleaned and deduplicated data](/result/S3/S3%20Silver.jpg)

---

## 3.4 Create Glue ETL Job 3: Silver → Gold

This is the most critical job - it computes business KPIs and **registers the results as external tables in the Glue Data Catalog**, making them directly queryable by Athena.

| Field | Value |
|-------|-------|
| Name | `silver-to-gold-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Worker type | G.1X |
| Number of workers | 2 |
| Script path | `s3://customer-behavior-lakehouse1/scripts/silver_to_gold_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**What this job does (`silver_to_gold_job.py`) - key sections:**

```python
import sys, boto3
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, count, countDistinct, sum, avg, to_date, lit
from awsglue.context import GlueContext
from awsglue.job import Job

# ... initialization ...

DATABASE_NAME = "customer_behavior_catalog_db"
BUCKET_NAME = "customer-behavior-lakehouse1"
SILVER_PATH = f"s3://{BUCKET_NAME}/silver/"
GOLD_PATH = f"s3://{BUCKET_NAME}/gold/"

glue = boto3.client("glue")

# Read Silver data
events = spark.read.parquet(f"{SILVER_PATH}events/")
orders = spark.read.parquet(f"{SILVER_PATH}orders/")
orders = orders.withColumn("order_date", to_date(col("order_time")))

# Compute 7 KPI aggregations
event_summary = events.groupBy("event_type").agg(count("*").alias("total_events"))
daily_revenue = orders.groupBy("order_date").agg(sum("total_usd").alias("total_revenue"))
payment_summary = orders.groupBy("payment_method").agg(
    count("order_id").alias("total_orders"),
    sum("total_usd").alias("total_revenue"),
    avg("total_usd").alias("avg_order_value")
)
country_revenue = orders.groupBy("country").agg(
    count("order_id").alias("total_orders"),
    sum("total_usd").alias("total_revenue"),
    avg("total_usd").alias("avg_order_value")
)
device_summary   = orders.groupBy("device").agg(...)
source_summary   = orders.groupBy("source").agg(...)
dashboard_summary = orders.agg(
    countDistinct("order_id").alias("total_orders"),
    countDistinct("customer_id").alias("total_customers"),
    sum("total_usd").alias("total_revenue"),
    avg("total_usd").alias("avg_order_value")
).withColumn("total_events", lit(events.count()))

# Write Parquet to Gold + register in Glue Catalog
write_gold_table("event_summary", event_summary)
write_gold_table("daily_revenue", daily_revenue)
write_gold_table("payment_summary", payment_summary)
write_gold_table("country_revenue", country_revenue)
write_gold_table("device_summary", device_summary)
write_gold_table("source_summary", source_summary)
write_gold_table("dashboard_summary", dashboard_summary)
```

The `write_gold_table()` function automatically:
1. Writes Parquet to `s3://.../gold/<table_name>/`
2. Calls `glue.delete_table()` (if exists - idempotent)
3. Calls `glue.create_table()` to register the schema in Glue Data Catalog

Run the job and wait for **Succeeded** (~8–12 minutes).

**Validate Gold output:**
```bash
# Check S3 Gold has 7 subdirectories
aws s3 ls s3://customer-behavior-lakehouse1/gold/ --recursive | head -30

# Check Glue Catalog tables are registered
aws glue get-tables \
    --database-name customer_behavior_catalog_db \
    --query "TableList[].Name"
```

**Expected Glue tables:**
```json
["country_revenue", "daily_revenue", "dashboard_summary",
 "device_summary", "event_summary", "payment_summary", "source_summary"]
```

![Glue Catalog Tables - 7 Gold tables registered and queryable](/result/AWS%20Glue/Glue%20Tables.jpg)

![S3 Gold - 7 KPI aggregation directories](/result/S3/S3%20Gold.jpg)

---

## 3.5 View All Jobs in Glue Console

After creating all three jobs, you should see them listed in the Glue Jobs console:

![AWS Glue ETL Jobs - all 3 jobs listed with status](/result/AWS%20Glue/AWS%20Glue%20Jobs.jpg)

---

## 3.6 Test & Error Handling

**Check job logs if a run fails:**

**AWS Console → AWS Glue → Jobs → [job name] → Runs → [failed run] → Error logs**

Or via CLI:
```bash
# Get job run status and error
aws glue get-job-runs --job-name silver-to-gold-job \
    --query "JobRuns[0].{Status:JobRunState,Error:ErrorMessage,Start:StartedOn}"

# Tail job output logs in CloudWatch
aws logs tail /aws-glue/jobs/output --follow
```

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `EntityNotFoundException: Database not found` | Glue catalog database not created | Complete Step 3.1 first |
| `AccessDeniedException` | IAM role missing S3 or Glue permissions | Attach required policies to `AWSGlueServiceRole-lakehouse` |
| `AnalysisException: Path does not exist` | Bronze/Silver data not yet written | Run Job 1 before Job 2, Job 2 before Job 3 |
| `FileNotFoundException` for events path | Firehose path doesn't match script hardcoded path | Update `events_path` in `raw_to_bronze_job.py` to match actual S3 path |
| Job timeout | Large dataset / insufficient workers | Increase Number of workers to 4 |

---

## 3.7 Expected Results Summary

After all 3 jobs succeed:

| Tier | Location | Format | Tables |
|------|----------|--------|--------|
| **Bronze** | `s3://.../bronze/` | Parquet | 7 tables (6 CSV + events) |
| **Silver** | `s3://.../silver/` | Parquet | 7 tables (deduplicated, normalized) |
| **Gold** | `s3://.../gold/` | Parquet | 7 KPI aggregation tables |
| **Glue Catalog** | `customer_behavior_catalog_db` | - | 7 external tables pointing to Gold |

✅ **Step 3 complete** - Proceed to [Step 4: Amazon Athena Queries](../5.4.4-Athena/)
