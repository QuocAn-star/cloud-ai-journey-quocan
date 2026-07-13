---
title: "Bước 2: S3 & Tải dữ liệu"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

# Bước 2: S3 Buckets & Tải Dữ liệu

Trong bước này, bạn sẽ tạo S3 bucket với cấu trúc prefix Medallion Architecture, cấu hình mã hóa và tải các file dữ liệu mẫu lên tầng Raw.

**Thời gian ước tính:** 20–30 phút

---

## Điều kiện tiên quyết

- AWS CLI được cấu hình với quyền `AmazonS3FullAccess` và `IAMFullAccess`
- File CSV dữ liệu mẫu đã sẵn sàng (xem Phần 5.2 để xem script tạo dữ liệu)

---

## 2.1 Tạo S3 Bucket

**AWS Console → S3 → Create bucket**

| Trường | Giá trị |
|--------|---------|
| Bucket name | `customer-behavior-lakehouse1` |
| AWS Region | `us-east-1` |
| Object Ownership | ACLs disabled (khuyến nghị) |
| Block all public access | ✅ Bật (giữ tất cả blocks) |
| Bucket versioning | Enable (khuyến nghị để phục hồi dữ liệu) |
| Default encryption | Server-side encryption với Amazon S3 managed keys (SSE-S3) |

Click **Create bucket**.

> 💡 **Lưu ý:** Tên S3 bucket là duy nhất toàn cầu. Nếu `customer-behavior-lakehouse1` đã được dùng, thêm Account ID của bạn: `customer-behavior-lakehouse1-<account-id>`. Cập nhật tất cả tham chiếu trong ETL scripts tương ứng.

**Tùy chọn CLI:**
```bash
aws s3api create-bucket \
    --bucket customer-behavior-lakehouse1 \
    --region us-east-1

# Bật versioning
aws s3api put-bucket-versioning \
    --bucket customer-behavior-lakehouse1 \
    --versioning-configuration Status=Enabled

# Bật mã hóa (SSE-S3)
aws s3api put-bucket-encryption \
    --bucket customer-behavior-lakehouse1 \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

---

## 2.2 Tạo Cấu trúc Thư mục (S3 Prefixes)

Trong bucket, tạo các "thư mục" (S3 prefix) cấp cao nhất sau:

```bash
# Tạo tất cả prefix cần thiết
aws s3api put-object --bucket customer-behavior-lakehouse1 --key raw/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key bronze/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key silver/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key gold/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key athena-results/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key scripts/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key tmp/
```

Hoặc qua Console: Trong bucket, click **Create folder** cho từng: `raw`, `bronze`, `silver`, `gold`, `athena-results`, `scripts`, `tmp`.

---

## 2.3 Tải File Dữ liệu Mẫu lên Tầng Raw

Tải tất cả 6 file CSV lên prefix `raw/`:

```bash
# Tải từng file CSV lên S3 Raw
aws s3 cp customers.csv    s3://customer-behavior-lakehouse1/raw/customers.csv
aws s3 cp orders.csv       s3://customer-behavior-lakehouse1/raw/orders.csv
aws s3 cp products.csv     s3://customer-behavior-lakehouse1/raw/products.csv
aws s3 cp order_items.csv  s3://customer-behavior-lakehouse1/raw/order_items.csv
aws s3 cp reviews.csv      s3://customer-behavior-lakehouse1/raw/reviews.csv
aws s3 cp sessions.csv     s3://customer-behavior-lakehouse1/raw/sessions.csv

# Xác minh tất cả upload thành công
aws s3 ls s3://customer-behavior-lakehouse1/raw/
```

**Kết quả mong đợi:**
```
2026-07-06 10:00:00    350000 customers.csv
2026-07-06 10:00:01   1200000 orders.csv
2026-07-06 10:00:01    220000 products.csv
2026-07-06 10:00:02    450000 order_items.csv
2026-07-06 10:00:02    180000 reviews.csv
2026-07-06 10:00:03    320000 sessions.csv
```

![S3 Raw - File CSV đã tải lên (dữ liệu nguồn gốc)](/result/S3/S3%20Raw%20-%20d%E1%BB%AF%20li%E1%BB%87u%20g%E1%BB%91c.jpg)

---

## 2.4 Kiểm tra Streaming Firehose (Tùy chọn)

Nếu bạn muốn test đường streaming qua Firehose:

**Bước A: Tạo Firehose Delivery Stream**

**AWS Console → Amazon Data Firehose → Create Firehose stream**

| Trường | Giá trị |
|--------|---------|
| Source | Direct PUT |
| Destination | Amazon S3 |
| Firehose stream name | `lakehouse-event-stream` |
| S3 bucket | `customer-behavior-lakehouse1` |
| S3 prefix | `raw/streaming/events/!{timestamp:yyyy}/!{timestamp:MM}/!{timestamp:dd}/!{timestamp:HH}/` |
| S3 error prefix | `raw/streaming/errors/` |
| Buffer size | 1 MB |
| Buffer interval | 60 giây |

**Bước B: Gửi sự kiện test**

```bash
aws firehose put-record \
    --delivery-stream-name lakehouse-event-stream \
    --record '{
        "Data": "{\"event_type\": \"page_view\", \"customer_id\": \"CUST-0001\", \"product_id\": \"PROD-042\", \"timestamp\": \"2026-07-10T10:00:00Z\"}\n"
    }'
```

**Bước C: Đợi và xác minh**

Đợi 60–90 giây (thời gian đệm Firehose), sau đó xác minh dữ liệu đã xuất hiện trong S3:

```bash
aws s3 ls s3://customer-behavior-lakehouse1/raw/streaming/ --recursive
```

![Firehose streaming data đã đổ vào S3 raw/streaming/](/result/S3/FirehoseStreaming%20%C4%91%C3%A3%20%C4%91%E1%BB%95%20data%20v%C3%A0o%20S3.jpg)

---

## 2.5 Tạo IAM Role cho Glue ETL Jobs

Tạo IAM role mà các Glue ETL job sẽ sử dụng để đọc và ghi vào S3.

**AWS Console → IAM → Roles → Create role**

| Trường | Giá trị |
|--------|---------|
| Trusted entity type | AWS service |
| Service | Glue |
| Use case | Glue |

**Thêm permissions - gán các policy sau:**
- `AWSGlueServiceRole` (managed) - cho phép Glue ghi CloudWatch logs
- `AmazonS3FullAccess` - để đơn giản cho workshop
- `AmazonAthenaFullAccess` - để Glue → đăng ký Catalog trong `silver_to_gold_job`

**Tên role:** `AWSGlueServiceRole-lakehouse`

> ⚠️ **Lưu ý quyền hạn tối thiểu:** Trong production, thay các policy broad bằng custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/raw/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/bronze/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/silver/*",
        "arn:aws:s3:::customer-behavior-lakehouse1"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:DeleteObject"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/bronze/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/silver/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/gold/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/scripts/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/tmp/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:*", "athena:*"],
      "Resource": "*"
    }
  ]
}
```

---

## 2.6 Tải Scripts ETL lên S3

Tải ba Glue ETL scripts lên S3 để Glue có thể truy cập:

```bash
# Tải tất cả scripts
aws s3 cp source_code/raw_to_bronze_job.py    s3://customer-behavior-lakehouse1/scripts/raw_to_bronze_job.py
aws s3 cp source_code/bronze_to_silver_job.py s3://customer-behavior-lakehouse1/scripts/bronze_to_silver_job.py
aws s3 cp source_code/silver_to_gold_job.py   s3://customer-behavior-lakehouse1/scripts/silver_to_gold_job.py

# Xác minh
aws s3 ls s3://customer-behavior-lakehouse1/scripts/
```

---

## 2.7 Kiểm tra & Xác nhận

```bash
# Liệt kê tất cả prefix để xác nhận cấu trúc
echo "=== Cấu trúc S3 Bucket ==="
aws s3 ls s3://customer-behavior-lakehouse1/

# Kiểm tra raw/ chứa đủ 6 file CSV
echo "=== File CSV Raw ==="
aws s3 ls s3://customer-behavior-lakehouse1/raw/

# Kiểm tra versioning
echo "=== Versioning ==="
aws s3api get-bucket-versioning --bucket customer-behavior-lakehouse1

# Kiểm tra mã hóa
echo "=== Mã hóa ==="
aws s3api get-bucket-encryption --bucket customer-behavior-lakehouse1 \
    --query "ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm"
```

**Kết quả mong đợi:**
- 7 prefix hiển thị: `raw/`, `bronze/`, `silver/`, `gold/`, `athena-results/`, `scripts/`, `tmp/`
- 6 file CSV trong `raw/`
- Versioning: `{ "Status": "Enabled" }`
- Mã hóa: `"AES256"`

---

## Xử lý sự cố

| Vấn đề | Nguyên nhân | Cách khắc phục |
|--------|-------------|----------------|
| `BucketAlreadyExists` | Tên bucket đã được dùng toàn cầu | Dùng tên duy nhất: thêm Account ID |
| `AccessDenied` khi tải lên | Thiếu quyền ghi S3 | Gán `AmazonS3FullAccess` cho IAM user |
| Dữ liệu Firehose không hiện trong S3 | Buffer interval chưa hết | Đợi 60–90 giây |
| Tải script thất bại | Thiếu prefix `scripts/` | Chạy `aws s3api put-object --bucket ... --key scripts/` trước |

✅ **Bước 2 hoàn thành** - Tiến hành đến [Bước 3: AWS Glue ETL Jobs](../5.4.3-Glue/)
