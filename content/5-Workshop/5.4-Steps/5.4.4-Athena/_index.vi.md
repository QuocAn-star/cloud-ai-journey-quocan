---
title: "Bước 4: Amazon Athena"
date: 2024-01-01
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

# Bước 4: Truy vấn Amazon Athena

Trong bước này, bạn sẽ cấu hình Amazon Athena để truy vấn các bảng tầng Gold đã đăng ký trong Glue Data Catalog, xác minh kết quả pipeline và khám phá dữ liệu bằng các truy vấn nghiệp vụ.

**Thời gian ước tính:** 15–20 phút

---

## Điều kiện tiên quyết

- Bước 3 hoàn thành (Glue ETL jobs chạy thành công, 7 bảng trong Glue Catalog)
- Prefix `athena-results/` trong S3 đã tồn tại

---

## 4.1 Cấu hình Vị trí Kết quả Truy vấn Athena

**AWS Console → Amazon Athena → Query editor → Settings → Manage**

| Trường | Giá trị |
|--------|---------|
| Query result location | `s3://customer-behavior-lakehouse1/athena-results/` |
| Encryption | SSE-S3 |

Click **Save**.

> ⚠️ **Quan trọng:** Athena không thể chạy truy vấn cho đến khi cấu hình vị trí kết quả. Bước này là bắt buộc.

**Tùy chọn CLI:**
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

## 4.2 Cấu hình Athena Workgroup (FinOps Best Practice)

Tạo Workgroup riêng với kiểm soát chi phí mỗi truy vấn:

**AWS Console → Athena → Administration → Workgroups → Create workgroup**

| Trường | Giá trị |
|--------|---------|
| Workgroup name | `lakehouse-wg` |
| Query result location | `s3://customer-behavior-lakehouse1/athena-results/` |
| Encrypt query results | ✅ SSE-S3 |
| Override client-side settings | ✅ Bật |
| **Kiểm soát sử dụng dữ liệu** | |
| - Per-query limit | 1 GB |
| - Hành động nếu truy vấn vượt giới hạn | Cancel query |

Click **Create workgroup**.

> 💡 **FinOps note:** Giới hạn 1 GB mỗi truy vấn đóng vai trò như lưới bảo vệ - bất kỳ truy vấn runaway nào quét quá nhiều dữ liệu sẽ tự động bị hủy trước khi phát sinh chi phí quá mức. Với $5/TB, 1 GB = tối đa $0.005 mỗi truy vấn.

---

## 4.3 Chọn Database trong Query Editor

Trong Athena Query Editor:
- **Data source**: `AwsDataCatalog`
- **Database**: `customer_behavior_catalog_db`
- **Workgroup**: `lakehouse-wg`

Bạn sẽ thấy 7 bảng trong panel bên trái:
- `dashboard_summary`
- `daily_revenue`
- `event_summary`
- `country_revenue`
- `device_summary`
- `payment_summary`
- `source_summary`

---

## 4.4 Tạo External Tables (Phương án Thủ công)

Nếu Glue ETL Job 3 không tự đăng ký bảng (hoặc để xác minh thủ công), chạy các câu lệnh `CREATE TABLE` từ `athena_create_tables.sql`:

```sql
-- Bảng Dashboard Summary
CREATE EXTERNAL TABLE IF NOT EXISTS dashboard_summary (
    total_orders    BIGINT,
    total_customers BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE,
    total_events    BIGINT
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/dashboard_summary/';

-- Bảng Daily Revenue
CREATE EXTERNAL TABLE IF NOT EXISTS daily_revenue (
    order_date    DATE,
    total_revenue DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/daily_revenue/';

-- Bảng Event Summary
CREATE EXTERNAL TABLE IF NOT EXISTS event_summary (
    event_type   STRING,
    total_events BIGINT
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/event_summary/';

-- Bảng Country Revenue
CREATE EXTERNAL TABLE IF NOT EXISTS country_revenue (
    country         STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/country_revenue/';

-- Bảng Device Summary
CREATE EXTERNAL TABLE IF NOT EXISTS device_summary (
    device          STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/device_summary/';

-- Bảng Payment Summary
CREATE EXTERNAL TABLE IF NOT EXISTS payment_summary (
    payment_method  STRING,
    total_orders    BIGINT,
    total_revenue   DOUBLE,
    avg_order_value DOUBLE
)
STORED AS PARQUET
LOCATION 's3://customer-behavior-lakehouse1/gold/payment_summary/';

-- Bảng Source Summary
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

## 4.5 Chạy Các Truy vấn Nghiệp vụ & Xác nhận Kết quả

Thực thi các truy vấn sau từ `athena_queries.sql` để xác minh kết quả pipeline:

### Truy vấn 1: Chỉ số Dashboard Tổng quan

```sql
SELECT * FROM dashboard_summary;
```

**Kết quả mong đợi:** 1 hàng với tổng đơn hàng, khách hàng, doanh thu, giá trị đơn hàng trung bình và tổng sự kiện.

![Athena - Kết quả truy vấn Dashboard Summary](/result/Athenas/Dashboard%20Summary.jpg)

---

### Truy vấn 2: Xu hướng Doanh thu Hàng ngày

```sql
SELECT *
FROM daily_revenue
ORDER BY order_date;
```

**Kết quả mong đợi:** ~365 hàng, mỗi ngày một hàng, hiển thị tổng doanh thu theo ngày.

![Athena - Truy vấn Daily Revenue trong editor](/result/Athenas/daily%20revenue.jpg)

![Athena - Dữ liệu kết quả Daily Revenue](/result/Athenas/result_daily_revenue.jpg)

---

### Truy vấn 3: Tần suất Sự kiện

```sql
SELECT *
FROM event_summary
ORDER BY total_events DESC;
```

**Kết quả mong đợi:** 5–8 hàng hiển thị các loại sự kiện (page_view, add_to_cart, purchase, checkout, v.v.) được sắp xếp theo tần suất.

![Athena - Kết quả truy vấn Event Summary](/result/Athenas/Event%20Summary.jpg)

---

### Truy vấn 4: Doanh thu theo Quốc gia

```sql
SELECT *
FROM country_revenue
ORDER BY total_revenue DESC
LIMIT 10;
```

**Kết quả mong đợi:** Các quốc gia được sắp xếp theo tổng doanh thu - ví dụ: US, UK, DE, FR, JP, VN, SG.

---

### Truy vấn 5: Doanh thu theo Phương thức Thanh toán

```sql
SELECT *
FROM payment_summary
ORDER BY total_revenue DESC;
```

**Kết quả mong đợi:** 3 hàng: credit_card, paypal, bank_transfer.

---

### Truy vấn 6: Doanh thu theo Loại Thiết bị

```sql
SELECT *
FROM device_summary
ORDER BY total_revenue DESC;
```

**Kết quả mong đợi:** 3 hàng: mobile, desktop, tablet.

---

### Truy vấn 7: Doanh thu theo Nguồn Traffic

```sql
SELECT *
FROM source_summary
ORDER BY total_revenue DESC;
```

**Kết quả mong đợi:** 4 hàng: organic, social, email, paid_ads.

---

## 4.6 Kiểm tra Metric & Chi phí

Sau khi chạy truy vấn, xác minh metric hiệu suất:

**Dữ liệu được quét mỗi truy vấn:**

Trong Athena Query Editor, sau mỗi truy vấn hoàn thành, xem metric **Data scanned** hiển thị bên dưới kết quả. Với định dạng Parquet trên các bảng Gold nhỏ gọn:
- `dashboard_summary` → ~5–20 KB được quét
- `daily_revenue` → ~10–50 KB được quét
- `country_revenue` → ~5–20 KB được quét

Điều này cực kỳ hiệu quả so với quét CSV thô (sẽ quét 1–10 MB mỗi truy vấn).

**Kiểm tra CloudWatch metrics cho Athena:**
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

## 4.7 Kiểm thử Các Kịch bản Lỗi

**Test 1: Truy vấn bảng không tồn tại**
```sql
SELECT * FROM non_existent_table;
```
Lỗi mong đợi: `TABLE_NOT_FOUND: Table does not exist`

**Test 2: Kích hoạt giới hạn chi phí workgroup**
```sql
-- Sẽ thất bại nếu bảng Silver được đăng ký và lớn hơn 1 GB
SELECT * FROM silver_orders;
```
Kết quả mong đợi: `Query cancelled - data usage limit exceeded` (bảo vệ workgroup hoạt động)

**Test 3: Xử lý lỗi syntax**
```sql
SELECT FROM dashboard_summary;
```
Lỗi mong đợi: `SYNTAX_ERROR: mismatched input 'FROM'`

---

## 4.8 Tóm tắt Kết quả Mong đợi

| Bảng | Số hàng mong đợi | Insight nghiệp vụ chính |
|------|------------------|-------------------------|
| `dashboard_summary` | 1 hàng | Tổng đơn hàng, khách hàng, doanh thu, giá trị đơn TB, tổng sự kiện |
| `daily_revenue` | ~365 hàng | Doanh thu mỗi ngày cho thấy xu hướng tăng/giảm |
| `event_summary` | ~5–8 hàng | Hành động người dùng thường xuyên nhất trên nền tảng |
| `country_revenue` | ~7–10 hàng | Khu vực địa lý nào tạo nhiều doanh thu nhất |
| `device_summary` | 3 hàng | Tỷ lệ doanh thu Mobile vs Desktop vs Tablet |
| `payment_summary` | 3 hàng | Ưu thích Credit Card vs PayPal vs Bank Transfer |
| `source_summary` | 4 hàng | Hiệu quả Organic vs Paid vs Social vs Email |

---

## Xử lý sự cố

| Vấn đề | Nguyên nhân | Cách khắc phục |
|--------|-------------|----------------|
| `HIVE_METASTORE_ERROR: Database not found` | Chọn sai database trong Query Editor | Chọn `customer_behavior_catalog_db` trong dropdown |
| `No output location provided` | Chưa cấu hình vị trí kết quả truy vấn | Hoàn thành Bước 4.1 - đặt result location |
| Truy vấn trả về 0 hàng | Bảng Gold trống (Job 3 thất bại) | Chạy lại `silver-to-gold-job` và kiểm tra thành công |
| `TABLE_NOT_FOUND` | Bảng chưa được Job 3 đăng ký | Chạy câu lệnh CREATE TABLE ở Bước 4.4 thủ công |

✅ **Bước 4 hoàn thành** - Tiến hành đến [Bước 5: Deploy Streamlit Dashboard trên EC2](../5.4.5-EC2-Dashboard/)
