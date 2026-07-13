---
title: "Worklog Tuần 2"
date: 2026-04-27
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

**Thời gian:** 27/04/2026 - 01/05/2026

## Mục tiêu tuần 2

- Thiết kế kiến trúc tổng thể AWS Data Lakehouse cho dự án Customer Behavior Analytics.
- Chuẩn bị môi trường AWS và tổ chức cấu trúc lưu trữ dữ liệu.
- Xây dựng luồng xử lý dữ liệu cho cả Batch Processing và Streaming Processing.
- Lập kế hoạch triển khai kiến trúc Medallion với ba tầng dữ liệu: Bronze, Silver và Gold.

## Công việc đã thực hiện

- Thiết kế kiến trúc tổng thể cho hệ thống **FinOps-Optimized Serverless Medallion Data Lakehouse**.
- Xác định vai trò của từng lớp trong kiến trúc:
  - Ingestion Layer.
  - Storage Layer.
  - Processing Layer.
  - Query Layer.
  - Visualization Layer.
- Thiết kế hai luồng tiếp nhận dữ liệu:
  - Batch Processing để đồng bộ dữ liệu từ cơ sở dữ liệu theo lịch.
  - Streaming Processing để thu thập sự kiện người dùng theo thời gian thực.
- Thiết lập cấu trúc lưu trữ trên Amazon S3 theo mô hình Medallion:
  - Raw Layer.
  - Bronze Layer.
  - Silver Layer.
  - Gold Layer.
- Xây dựng quy ước tổ chức thư mục và lưu trữ dữ liệu phục vụ cho quá trình phân tích.
- Nghiên cứu và xác định vai trò của các dịch vụ AWS sẽ được tích hợp trong từng giai đoạn của hệ thống:
  - Amazon API Gateway.
  - Amazon Kinesis Data Firehose.
  - AWS Lambda.
  - AWS Glue ETL.
  - AWS Glue Data Catalog.
  - Amazon Athena.
  - Amazon EC2.
- Chuẩn bị môi trường phát triển để triển khai pipeline ETL và Dashboard trong các tuần tiếp theo.

## Kết quả đạt được

- Hoàn thành thiết kế kiến trúc tổng thể cho hệ thống Customer Behavior Analytics trên nền tảng AWS.
- Xây dựng được luồng dữ liệu hoàn chỉnh từ khâu tiếp nhận dữ liệu đến trực quan hóa kết quả phân tích.
- Hoàn thiện cấu trúc lưu trữ dữ liệu theo mô hình Medallion trên Amazon S3.
- Chuẩn bị đầy đủ môi trường và kế hoạch triển khai cho các bước xây dựng ETL Pipeline ở những tuần tiếp theo.
- Tạo nền tảng vững chắc để phát triển các tầng Bronze, Silver và Gold trong giai đoạn triển khai.