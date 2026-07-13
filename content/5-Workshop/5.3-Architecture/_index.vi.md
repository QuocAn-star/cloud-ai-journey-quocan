---
title: "Mô tả Kiến trúc"
date: 2024-01-01
weight: 3
chapter: false
pre: " <b> 5.3 </b> "
---

# Mô tả Kiến trúc

## Kiến trúc Tổng quan

Nền tảng triển khai mô hình **Serverless Medallion Data Lakehouse** - dữ liệu chảy qua bốn tầng S3 (Raw → Bronze → Silver → Gold), được xử lý bởi AWS Glue ETL jobs, truy vấn bởi Amazon Athena, và trực quan hóa trên Streamlit Dashboard được lưu trữ trên EC2 trong VPC.

---

## Mô tả từng Lớp

### Lớp 1: VPC & Networking

Toàn bộ nền tảng chạy trong một **Amazon VPC** để đảm bảo cách ly mạng và bảo mật.

```
VPC: 10.0.0.0/16
 └── Public Subnet: 10.0.1.0/24 (us-east-1a)
      └── EC2 Instance (Streamlit Dashboard)
           └── Elastic IP (IP tĩnh public)
 └── Internet Gateway → gắn vào VPC
 └── Route Table → 0.0.0.0/0 → Internet Gateway
 └── Security Group (EC2):
      Inbound: port 22 (SSH), port 8501 (Streamlit)
      Outbound: tất cả traffic
```

**Tại sao cần VPC?** Chạy EC2 trong VPC đảm bảo dashboard không thể truy cập từ các nguồn internet tùy ý. Security Group hoạt động như tường lửa stateful - chỉ các port được cho phép rõ ràng (22 cho quản lý SSH, 8501 cho Streamlit) mới được mở.

![VPC Dashboard - Danh sách Your VPCs](/result/VPC/Your%20VPCs..jpg)

![Subnets - Public subnet trong VPC](/result/VPC/Subnets.jpg)

![Internet Gateway gắn vào VPC](/result/VPC/Internet%20Gateway.jpg)

![Route Tables - Route 0.0.0.0/0 tới IGW](/result/VPC/Route%20Tables.jpg)

![Security Group - Inbound rules cho port 22 và 8501](/result/VPC/Security%20Group.jpg)

---

### Lớp 2: S3 Data Lake - Kiến trúc Medallion

Bốn prefix trong một S3 bucket tạo thành các tầng data lake:

```
s3://customer-behavior-lakehouse1/
├── raw/                          ← Dữ liệu nguồn gốc (CSV + JSON streaming)
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── order_items.csv
│   ├── reviews.csv
│   ├── sessions.csv
│   └── streaming/events/2026/07/06/08/   ← JSON do Firehose gửi đến
│
├── bronze/                       ← Chuyển đổi sang Parquet, không transform
│   ├── customers/
│   ├── orders/
│   ├── products/
│   ├── order_items/
│   ├── reviews/
│   ├── sessions/
│   └── events/
│
├── silver/                       ← Làm sạch, loại trùng, chuẩn hóa schema
│   └── [cùng cấu trúc bảng như bronze]
│
├── gold/                         ← Tổng hợp KPI nghiệp vụ (đăng ký trong Glue Catalog)
│   ├── event_summary/
│   ├── daily_revenue/
│   ├── payment_summary/
│   ├── country_revenue/
│   ├── device_summary/
│   ├── source_summary/
│   └── dashboard_summary/
│
└── athena-results/               ← Lưu trữ kết quả truy vấn Athena
```

**Tầng Raw** - dữ liệu gốc nguyên bản từ hệ thống nguồn (file CSV và JSON Firehose):

![S3 Raw - Dữ liệu nguồn gốc](/result/S3/S3%20Raw%20-%20d%E1%BB%AF%20li%E1%BB%87u%20g%E1%BB%91c.jpg)

**Dữ liệu streaming Firehose** gửi đến Raw/streaming/:

![Firehose streaming data đã đổ vào S3](/result/S3/FirehoseStreaming%20%C4%91%C3%A3%20%C4%91%E1%BB%95%20data%20v%C3%A0o%20S3.jpg)

**Tầng Bronze** - định dạng Parquet, schema giữ nguyên từ Raw:

![S3 Bronze - Dữ liệu đã chuyển sang Parquet](/result/S3/S3%20Bronze.jpg)

**Tầng Silver** - dữ liệu sạch, đã loại trùng, chuẩn hóa:

![S3 Silver - Dữ liệu đã làm sạch](/result/S3/S3%20Silver.jpg)

**Tầng Gold** - tổng hợp KPI nghiệp vụ sẵn sàng cho Athena:

![S3 Gold - Dữ liệu tổng hợp KPI](/result/S3/S3%20Gold.jpg)

---

### Lớp 3: Tầng Tiếp nhận

**Đường Streaming (Firehose → S3 Raw):**
- Amazon API Gateway nhận HTTP POST events từ client
- Events được proxy tới Amazon Data Firehose
- Firehose đệm events (60 giây hoặc 1 MB) và gửi đến `s3://.../raw/streaming/`
- Lambda function có thể gắn vào Firehose để chuyển đổi nội tuyến

**Đường Batch (Lambda → S3 Raw):**
- Amazon EventBridge Scheduler kích hoạt theo lịch cron
- Kích hoạt Lambda function đọc từ cơ sở dữ liệu nguồn
- Lambda trích xuất bản ghi và ghi CSV vào `s3://.../raw/`

---

### Lớp 4: Tầng Xử lý - AWS Glue ETL

Ba Glue ETL job tuần tự xử lý dữ liệu qua các tầng Medallion:

**Job 1: `raw_to_bronze_job.py` - Raw → Bronze**

Đọc file CSV từ S3 Raw, chuyển đổi sang Parquet, và ghi vào Bronze. Cũng đọc JSON events streaming từ đường Firehose.

```python
BUCKET_NAME = "customer-behavior-lakehouse1"
RAW_PATH = f"s3://{BUCKET_NAME}/raw/"
BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"

# Xử lý từng bảng CSV
csv_tables = ["customers", "orders", "products", "order_items", "reviews", "sessions"]
for table in csv_tables:
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{RAW_PATH}{table}.csv")
    df.write.mode("overwrite").parquet(f"{BRONZE_PATH}{table}/")

# Xử lý Firehose streaming events (JSON)
events_df = spark.read.option("recursiveFileLookup", "true").json(
    f"s3://{BUCKET_NAME}/raw/streaming/events/2026/07/06/08/"
)
events_df.write.mode("overwrite").parquet(f"{BRONZE_PATH}events/")
```

**Job 2: `bronze_to_silver_job.py` - Bronze → Silver**

Áp dụng các chuyển đổi chất lượng dữ liệu:
- `dropDuplicates()` - loại bỏ các hàng trùng lặp hoàn toàn
- Chuẩn hóa tên cột (chữ thường, dấu gạch dưới)
- Cắt khoảng trắng cho tất cả cột StringType
- Phân tích timestamp cho các cột ngày/giờ

**Job 3: `silver_to_gold_job.py` - Silver → Gold**

Tính toán tổng hợp KPI nghiệp vụ và **tự động đăng ký kết quả vào Glue Data Catalog**:

| Bảng Gold | Nguồn | Mô tả |
|-----------|-------|-------|
| `event_summary` | events | Đếm số sự kiện theo loại |
| `daily_revenue` | orders | Tổng doanh thu mỗi ngày |
| `payment_summary` | orders | Đơn hàng + doanh thu theo phương thức thanh toán |
| `country_revenue` | orders | Đơn hàng + doanh thu theo quốc gia |
| `device_summary` | orders | Đơn hàng + doanh thu theo loại thiết bị |
| `source_summary` | orders | Đơn hàng + doanh thu theo nguồn traffic |
| `dashboard_summary` | orders + events | Tổng hợp (đơn hàng, khách hàng, doanh thu, sự kiện) |

Sau khi Job 3 chạy, các bảng này tự động có sẵn trong Athena mà không cần crawler thủ công.

![AWS Glue - Danh sách 3 ETL Jobs](/result/AWS%20Glue/AWS%20Glue%20Jobs.jpg)

![Glue Data Catalog Database - customer_behavior_catalog_db](/result/AWS%20Glue/Glue%20Database.jpg)

![Glue Catalog Tables - 7 bảng Gold đã đăng ký](/result/AWS%20Glue/Glue%20Tables.jpg)

---

### Lớp 5: Tầng Truy vấn - Amazon Athena

Amazon Athena đọc các bảng tầng Gold đã đăng ký trong Glue Data Catalog và thực thi truy vấn SQL một cách serverless - không cần cung cấp hạ tầng.

```sql
-- Chỉ số dashboard tổng quan
SELECT * FROM dashboard_summary;

-- Xu hướng doanh thu hàng ngày
SELECT * FROM daily_revenue ORDER BY order_date;

-- Top quốc gia theo doanh thu
SELECT * FROM country_revenue ORDER BY total_revenue DESC;

-- Tần suất sự kiện
SELECT * FROM event_summary ORDER BY total_events DESC;
```

**Ưu điểm FinOps:** Athena tính phí $5 mỗi TB quét. Các bảng Gold ở định dạng Parquet rất nhỏ gọn (thường 10–100 KB mỗi bảng cho dữ liệu workshop), làm mỗi truy vấn chỉ tốn một phần nhỏ của cent.

![Athena - Kết quả truy vấn Dashboard Summary](/result/Athenas/Dashboard%20Summary.jpg)

![Athena - Kết quả truy vấn Daily Revenue](/result/Athenas/daily%20revenue.jpg)

![Athena - Kết quả truy vấn Event Summary](/result/Athenas/Event%20Summary.jpg)

---

### Lớp 6: Tầng Trực quan hóa - Streamlit Dashboard trên EC2

Ứng dụng Streamlit (`app_beautiful.py`) chạy trên EC2 instance và truy vấn Athena qua `awswrangler`:

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

Dashboard hiển thị 8 biểu đồ tương tác + KPI cards bao phủ tất cả các chiều nghiệp vụ.

![EC2 Instance đang chạy Streamlit dashboard](/result/EC2/EC2%20Instance.jpg)

![EC2 Security Group - port 22 và 8501 mở](/result/EC2/Security%20Group.jpg)

**Các màn hình Dashboard:**

![Xu hướng Doanh thu - doanh thu hàng ngày theo thời gian](/result/DashBoard/Revenue%20Trend.png)

![Top 10 Quốc gia theo Doanh thu](/result/DashBoard/Top%2010%20Countries%20by%20Revenue.png)

![Doanh thu theo Loại Thiết bị](/result/DashBoard/Revenue%20by%20Device.png)

![Doanh thu theo Phương thức Thanh toán](/result/DashBoard/Revenue%20by%20Payment%20Method.png)

![Doanh thu theo Nguồn Traffic](/result/DashBoard/Revenue%20by%20Traffic%20Source.png)

![Phân phối Sự kiện theo loại](/result/DashBoard/Event%20Distribution.png)

![Bảng Top Performers tổng hợp](/result/DashBoard/Top%20Performers.jpg)

---

## Lý do Lựa chọn Dịch vụ

| Dịch vụ | Lý do chọn | Lựa chọn thay thế đã xem xét |
|---------|------------|-------------------------------|
| **Amazon S3** | Lưu trữ đối tượng bền vững rẻ nhất; trả theo GB lưu trữ | EFS (quá đắt), EBS (không chia sẻ được) |
| **AWS Glue** | PySpark managed hoàn toàn; trả theo DPU-second | EMR (cần quản lý cluster, chi phí cao hơn) |
| **Amazon Athena** | Trả theo TB quét; Parquet giảm quét 85% | Redshift ($700+/tháng cho cluster nhỏ nhất) |
| **Amazon Data Firehose** | Không cần lên kế hoạch dung lượng; đệm tích hợp | Kinesis Data Streams (cần quản lý shard) |
| **AWS Lambda** | Trả theo 100ms invocation; chi phí idle bằng 0 | EC2 worker (chi phí luôn hoạt động) |
| **Amazon EC2 (t3.micro)** | Đủ điều kiện Free Tier; đủ cho Streamlit web app | Fargate/App Runner (phức tạp hơn một chút) |
| **EventBridge Scheduler** | Cron serverless; 14M invocations miễn phí/tháng | EC2 cron (cần instance luôn hoạt động) |
| **Glue Data Catalog** | Miễn phí đến 1M đối tượng; metadata thống nhất cho Athena | Glue Crawlers theo lịch (tốn DPU-hour mỗi lần crawl) |

✅ **Đã hiểu kiến trúc** - Tiến hành đến [Các bước thực hành](../5.4-Steps/)
