---
title: "Bước 3: AWS Glue ETL"
date: 2024-01-01
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

# Bước 3: AWS Glue ETL Jobs

Trong bước này, bạn sẽ tạo Glue Data Catalog database và ba ETL job xử lý dữ liệu qua các tầng Medallion: **Raw → Bronze → Silver → Gold**.

**Thời gian ước tính:** 30–40 phút

> ⚠️ **Thứ tự quan trọng:** Luôn chạy Job 1 trước Job 2, và Job 2 trước Job 3. Mỗi job đọc từ output của tầng trước.

---

## Điều kiện tiên quyết

- Bước 2 hoàn thành (S3 bucket với dữ liệu Raw và scripts đã tải lên)
- IAM role `AWSGlueServiceRole-lakehouse` đã tạo (Bước 2.5)

---

## 3.1 Tạo Glue Data Catalog Database

**AWS Console → AWS Glue → Data Catalog → Databases → Add database**

| Trường | Giá trị |
|--------|---------|
| Database name | `customer_behavior_catalog_db` |
| Description | `Catalog for Customer Behavior Lakehouse Gold tables` |
| Location (tùy chọn) | `s3://customer-behavior-lakehouse1/gold/` |

Click **Create database**.

**Tùy chọn CLI:**
```bash
aws glue create-database \
    --database-input '{
        "Name": "customer_behavior_catalog_db",
        "Description": "Catalog for Customer Behavior Lakehouse Gold tables",
        "LocationUri": "s3://customer-behavior-lakehouse1/gold/"
    }'
```

![Glue Data Catalog Database - customer_behavior_catalog_db đã tạo](/result/AWS%20Glue/Glue%20Database.jpg)

---

## 3.2 Tạo Glue ETL Job 1: Raw → Bronze

**AWS Console → AWS Glue → ETL Jobs → Create job → Script editor (Spark)**

Chọn **Spark** làm engine. Dán toàn bộ nội dung của `raw_to_bronze_job.py` vào editor.

**Cấu hình job:**

| Trường | Giá trị |
|--------|---------|
| Name | `raw-to-bronze-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Language | Python 3 |
| Worker type | G.1X |
| Number of workers | 2 |
| Job timeout | 30 phút |
| Script path | `s3://customer-behavior-lakehouse1/scripts/raw_to_bronze_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**Job này làm gì (`raw_to_bronze_job.py`):**

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

# === Xử lý 6 bảng CSV ===
csv_tables = ["customers", "orders", "products", "order_items", "reviews", "sessions"]

for table in csv_tables:
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(f"{RAW_PATH}{table}.csv")
    )
    df.write.mode("overwrite").parquet(f"{BRONZE_PATH}{table}/")
    print(f"Đã lưu Bronze: {table}")

# === Xử lý Firehose streaming events ===
events_path = f"s3://{BUCKET_NAME}/raw/streaming/events/2026/07/06/08/"
events_df = spark.read.option("recursiveFileLookup", "true").json(events_path)
events_df.write.mode("overwrite").parquet(f"{BRONZE_PATH}events/")

print("Raw → Bronze hoàn thành.")
job.commit()
```

Click **Save** rồi **Run**.

**Theo dõi job:**
- Vào tab **Runs**
- Đợi status chuyển từ `Running` → `Succeeded` (~3–5 phút)

**Xác nhận output Bronze:**
```bash
aws s3 ls s3://customer-behavior-lakehouse1/bronze/ --recursive | head -20
```

Kết quả mong đợi: Các file Parquet part trong mỗi thư mục bảng dưới `bronze/`.

![S3 Bronze - File Parquet được tạo từ dữ liệu CSV](/result/S3/S3%20Bronze.jpg)

---

## 3.3 Tạo Glue ETL Job 2: Bronze → Silver

**AWS Console → AWS Glue → ETL Jobs → Create job → Script editor (Spark)**

| Trường | Giá trị |
|--------|---------|
| Name | `bronze-to-silver-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Worker type | G.1X |
| Number of workers | 2 |
| Script path | `s3://customer-behavior-lakehouse1/scripts/bronze_to_silver_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**Job này làm gì (`bronze_to_silver_job.py`):**

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, trim, to_timestamp
from pyspark.sql.types import StringType
from awsglue.context import GlueContext
from awsglue.job import Job

# ... khởi tạo ...

tables = ["customers", "orders", "products", "order_items", "reviews", "sessions", "events"]

def clean_column_name(name):
    return name.strip().lower().replace(" ", "_").replace("-", "_")

for table in tables:
    df = spark.read.parquet(f"{BRONZE_PATH}{table}/")

    # Bước 1: Loại bỏ hàng trùng lặp
    df = df.dropDuplicates()

    # Bước 2: Chuẩn hóa tên cột
    for old_col in df.columns:
        new_col = clean_column_name(old_col)
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)

    # Bước 3: Cắt khoảng trắng từ cột string
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, trim(col(field.name)))

    # Bước 4: Phân tích cột timestamp
    for column_name in df.columns:
        lower_name = column_name.lower()
        if "date" in lower_name or "time" in lower_name or "timestamp" in lower_name:
            df = df.withColumn(column_name, to_timestamp(col(column_name)))

    df.write.mode("overwrite").parquet(f"{SILVER_PATH}{table}/")

print("Bronze to Silver job hoàn thành.")
job.commit()
```

Chạy job và đợi status **Succeeded** (~5–8 phút).

**Xác nhận output Silver:**
```bash
aws s3 ls s3://customer-behavior-lakehouse1/silver/ --recursive | head -20
```

![S3 Silver - Dữ liệu đã làm sạch và loại trùng](/result/S3/S3%20Silver.jpg)

---

## 3.4 Tạo Glue ETL Job 3: Silver → Gold

Đây là job quan trọng nhất - tính toán KPI nghiệp vụ và **tự động đăng ký kết quả dưới dạng external table trong Glue Data Catalog**, làm chúng có thể truy vấn trực tiếp bởi Athena.

| Trường | Giá trị |
|--------|---------|
| Name | `silver-to-gold-job` |
| IAM Role | `AWSGlueServiceRole-lakehouse` |
| Glue version | Glue 4.0 |
| Worker type | G.1X |
| Number of workers | 2 |
| Script path | `s3://customer-behavior-lakehouse1/scripts/silver_to_gold_job.py` |
| Temporary path | `s3://customer-behavior-lakehouse1/tmp/` |

**Job này làm gì (`silver_to_gold_job.py`) - các phần chính:**

```python
DATABASE_NAME = "customer_behavior_catalog_db"
glue = boto3.client("glue")

# Đọc dữ liệu Silver
events = spark.read.parquet(f"{SILVER_PATH}events/")
orders = spark.read.parquet(f"{SILVER_PATH}orders/")
orders = orders.withColumn("order_date", to_date(col("order_time")))

# Tính 7 tổng hợp KPI
event_summary   = events.groupBy("event_type").agg(count("*").alias("total_events"))
daily_revenue   = orders.groupBy("order_date").agg(sum("total_usd").alias("total_revenue"))
payment_summary = orders.groupBy("payment_method").agg(
    count("order_id").alias("total_orders"),
    sum("total_usd").alias("total_revenue"),
    avg("total_usd").alias("avg_order_value")
)
country_revenue = orders.groupBy("country").agg(...)
device_summary  = orders.groupBy("device").agg(...)
source_summary  = orders.groupBy("source").agg(...)
dashboard_summary = orders.agg(
    countDistinct("order_id").alias("total_orders"),
    countDistinct("customer_id").alias("total_customers"),
    sum("total_usd").alias("total_revenue"),
    avg("total_usd").alias("avg_order_value")
).withColumn("total_events", lit(events.count()))

# Ghi Parquet sang Gold + đăng ký trong Glue Catalog
write_gold_table("event_summary", event_summary)
write_gold_table("daily_revenue", daily_revenue)
write_gold_table("payment_summary", payment_summary)
write_gold_table("country_revenue", country_revenue)
write_gold_table("device_summary", device_summary)
write_gold_table("source_summary", source_summary)
write_gold_table("dashboard_summary", dashboard_summary)
```

Hàm `write_gold_table()` tự động:
1. Ghi Parquet vào `s3://.../gold/<table_name>/`
2. Gọi `glue.delete_table()` (nếu tồn tại - idempotent)
3. Gọi `glue.create_table()` để đăng ký schema trong Glue Data Catalog

Chạy job và đợi **Succeeded** (~8–12 phút).

**Xác nhận output Gold:**
```bash
# Kiểm tra S3 Gold có 7 thư mục con
aws s3 ls s3://customer-behavior-lakehouse1/gold/ --recursive | head -30

# Kiểm tra các bảng Glue Catalog đã đăng ký
aws glue get-tables \
    --database-name customer_behavior_catalog_db \
    --query "TableList[].Name"
```

**Kết quả Glue tables mong đợi:**
```json
["country_revenue", "daily_revenue", "dashboard_summary",
 "device_summary", "event_summary", "payment_summary", "source_summary"]
```

![Glue Catalog Tables - 7 bảng Gold đã đăng ký và có thể truy vấn](/result/AWS%20Glue/Glue%20Tables.jpg)

![S3 Gold - 7 thư mục tổng hợp KPI](/result/S3/S3%20Gold.jpg)

---

## 3.5 Xem Tất cả Jobs trong Glue Console

Sau khi tạo cả ba jobs, bạn có thể thấy chúng trong Glue Jobs console:

![AWS Glue ETL Jobs - 3 jobs được liệt kê với trạng thái](/result/AWS%20Glue/AWS%20Glue%20Jobs.jpg)

---

## 3.6 Kiểm tra & Xử lý Lỗi

**Kiểm tra job logs nếu run thất bại:**

**AWS Console → AWS Glue → Jobs → [tên job] → Runs → [run thất bại] → Error logs**

Hoặc qua CLI:
```bash
# Lấy trạng thái và lỗi job run
aws glue get-job-runs --job-name silver-to-gold-job \
    --query "JobRuns[0].{Status:JobRunState,Error:ErrorMessage,Start:StartedOn}"

# Theo dõi output logs trong CloudWatch
aws logs tail /aws-glue/jobs/output --follow
```

**Các lỗi thường gặp và cách khắc phục:**

| Lỗi | Nguyên nhân | Cách khắc phục |
|-----|-------------|----------------|
| `EntityNotFoundException: Database not found` | Chưa tạo Glue catalog database | Hoàn thành Bước 3.1 trước |
| `AccessDeniedException` | IAM role thiếu quyền S3 hoặc Glue | Gán các policy cần thiết cho `AWSGlueServiceRole-lakehouse` |
| `AnalysisException: Path does not exist` | Dữ liệu Bronze/Silver chưa được ghi | Chạy Job 1 trước Job 2, Job 2 trước Job 3 |
| `FileNotFoundException` cho events path | Path Firehose không khớp với path hardcoded trong script | Cập nhật `events_path` trong `raw_to_bronze_job.py` để khớp với path S3 thực tế |
| Job timeout | Dataset lớn / không đủ workers | Tăng Number of workers lên 4 |

---

## 3.7 Tóm tắt Kết quả Mong đợi

Sau khi cả 3 job thành công:

| Tầng | Vị trí | Định dạng | Bảng |
|------|--------|-----------|------|
| **Bronze** | `s3://.../bronze/` | Parquet | 7 bảng (6 CSV + events) |
| **Silver** | `s3://.../silver/` | Parquet | 7 bảng (đã loại trùng, chuẩn hóa) |
| **Gold** | `s3://.../gold/` | Parquet | 7 bảng tổng hợp KPI |
| **Glue Catalog** | `customer_behavior_catalog_db` | - | 7 external table trỏ tới Gold |

✅ **Bước 3 hoàn thành** - Tiến hành đến [Bước 4: Amazon Athena Queries](../5.4.4-Athena/)
