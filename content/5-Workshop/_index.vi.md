---
title: "Workshop"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# FinOps-Optimized Serverless Medallion Data Lakehouse - Workshop

## Giới thiệu Workshop

Workshop thực hành này hướng dẫn bạn xây dựng một **data lakehouse hoàn toàn serverless, thuần cloud** trên AWS từ đầu. Bạn sẽ triển khai một pipeline dữ liệu end-to-end hoàn chỉnh để tiếp nhận, chuyển đổi và trực quan hóa dữ liệu hành vi khách hàng sử dụng **Kiến trúc Medallion** (Raw → Bronze → Silver → Gold), áp dụng **FinOps best practices** để giữ chi phí ở mức tối thiểu xuyên suốt.

Cuối workshop, bạn sẽ có một pipeline end-to-end hoàn chỉnh chạy trên tài khoản AWS của riêng mình.

## Những gì bạn sẽ xây dựng

```
Events từ Website/Mobile
        │
        ▼
  API Gateway ──► Firehose ──► Lambda (chuyển đổi nội tuyến)
                                       │
                                       ▼
                                  S3: Raw/Streaming
                                       │
  DB đơn hàng ──► EventBridge ──► Lambda ──► S3: Raw/Batch
                                       │
                              ┌────────┘
                              ▼
                      AWS Glue ETL Job 1
                      (Raw → Bronze: CSV sang Parquet)
                              │
                              ▼
                      AWS Glue ETL Job 2
                      (Bronze → Silver: Làm sạch, Loại bỏ trùng)
                              │
                              ▼
                      AWS Glue ETL Job 3
                      (Silver → Gold: Tổng hợp nghiệp vụ)
                              │
                        ┌─────┘
                        ▼
                  Glue Data Catalog
                        │
                        ▼
                  Amazon Athena (Truy vấn SQL)
                        │
                        ▼
              Streamlit Dashboard (EC2 + VPC)
```

## Các phần của Workshop

1. [Tổng quan](5.1-Overview/)
2. [Điều kiện tiên quyết](5.2-Prerequisite/)
3. [Mô tả kiến trúc](5.3-Architecture/)
4. [Các bước thực hành](5.4-Steps/)
   - [Bước 1: Thiết lập VPC & Mạng](5.4-Steps/5.4.1-VPC/)
   - [Bước 2: Tạo S3 Buckets & Lưu trữ](5.4-Steps/5.4.2-S3/)
   - [Bước 3: Tạo AWS Glue ETL Jobs](5.4-Steps/5.4.3-Glue/)
   - [Bước 4: Truy vấn với Amazon Athena](5.4-Steps/5.4.4-Athena/)
   - [Bước 5: Deploy Streamlit Dashboard trên EC2](5.4-Steps/5.4.5-EC2-Dashboard/)
   - [Bước 6: Giám sát với CloudWatch](5.4-Steps/5.4.6-Monitoring/)
5. [Dọn dẹp tài nguyên](5.5-Cleanup/)

## Thời gian & Chi phí ước tính

| Mục | Giá trị |
|-----|---------|
| **Thời gian** | ~3–4 giờ (toàn bộ workshop) |
| **Chi phí ước tính** | ~$1–3 USD (nếu dọn dẹp trong ngày) |
| **AWS Region** | `us-east-1` (N. Virginia) - khuyến nghị |
| **Độ khó** | Trung cấp |