---
title: "Các bước thực hành"
date: 2024-01-01
weight: 4
chapter: false
pre: " <b> 5.4 </b> "
---

# Các bước thực hành

Phần này hướng dẫn bạn từng bước triển khai end-to-end hoàn chỉnh **FinOps-Optimized Serverless Medallion Data Lakehouse** trên AWS.

---

## Tổng quan các Bước

| Bước | Chủ đề | Thời gian | Kết quả chính |
|------|--------|-----------|---------------|
| [5.4.1 VPC & Networking](5.4.1-VPC/) | Tạo VPC, subnet, IGW, security group | 15–20 phút | `lakehouse-vpc` sẵn sàng cho EC2 |
| [5.4.2 S3 & Tải dữ liệu](5.4.2-S3/) | Tạo S3 bucket, cấu trúc thư mục, tải CSV | 20–30 phút | 6 file CSV trong `raw/`, IAM role cho Glue |
| [5.4.3 AWS Glue ETL](5.4.3-Glue/) | Tạo 3 ETL jobs: Raw→Bronze→Silver→Gold | 30–40 phút | 7 bảng Gold đăng ký trong Glue Catalog |
| [5.4.4 Amazon Athena](5.4.4-Athena/) | Cấu hình Athena, chạy 7 truy vấn nghiệp vụ | 15–20 phút | Kết quả truy vấn đã xác minh |
| [5.4.5 EC2 & Dashboard](5.4.5-EC2-Dashboard/) | Khởi chạy EC2, deploy Streamlit dashboard | 25–35 phút | Dashboard trực tiếp tại `http://<ip>:8501` |
| [5.4.6 Giám sát](5.4.6-Monitoring/) | Thiết lập CloudWatch alarms và dashboard | 20–25 phút | 3 alarms + monitoring dashboard |

**Tổng thời gian ước tính:** 2–3 giờ cho tất cả các bước

---

## Quan trọng: Thực hiện các Bước theo Thứ tự

Mỗi bước xây dựng dựa trên bước trước. Không bỏ qua bước nào.

```
[5.4.1 VPC]              → cung cấp mạng cho EC2
    ↓
[5.4.2 S3 + IAM]         → cung cấp dữ liệu và roles cho Glue
    ↓
[5.4.3 Glue ETL]         → tạo ra các bảng Gold trong Glue Catalog
    ↓
[5.4.4 Athena]           → xác thực dữ liệu Gold qua SQL
    ↓
[5.4.5 EC2 Dashboard]    → trực quan hóa dữ liệu Gold từ Athena
    ↓
[5.4.6 Giám sát]         → quan sát toàn bộ pipeline
```

---

## Bắt đầu với Bước 1

→ [Bước 1: Thiết lập VPC & Networking](5.4.1-VPC/)
