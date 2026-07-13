---
title: "Worklog Tuần 3"
date: 2026-05-03
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
---

**Thời gian:** 04/05/2026 - 10/05/2026

## Mục tiêu tuần 3

- Triển khai tầng Ingestion Layer cho hệ thống Data Lakehouse.
- Xây dựng hai luồng tiếp nhận dữ liệu gồm Batch Processing và Streaming Processing.
- Thiết lập các dịch vụ AWS phục vụ quá trình thu thập dữ liệu.
- Kiểm tra dữ liệu được ghi thành công vào Amazon S3.

## Công việc đã thực hiện

- Thiết lập **Amazon API Gateway** để tiếp nhận dữ liệu từ các ứng dụng bên ngoài.
- Xây dựng **AWS Lambda** xử lý yêu cầu từ API Gateway và ghi dữ liệu vào hệ thống.
- Cấu hình **Amazon Kinesis Data Firehose** để tiếp nhận dữ liệu Streaming và lưu trực tiếp vào Amazon S3.
- Thiết lập **Amazon EventBridge Scheduler** để tự động kích hoạt quá trình đồng bộ dữ liệu theo lịch.
- Phát triển Lambda phục vụ luồng **Batch Processing** nhằm đồng bộ dữ liệu từ cơ sở dữ liệu lên Amazon S3.
- Kiểm tra luồng dữ liệu của cả hai pipeline:
  - Batch Processing.
  - Streaming Processing.
- Xác thực dữ liệu đã được ghi thành công vào thư mục **Raw Layer** trên Amazon S3.
- Theo dõi quá trình tiếp nhận dữ liệu bằng **Amazon CloudWatch Logs** để kiểm tra lỗi và đánh giá trạng thái hoạt động của hệ thống.

## Kết quả đạt được

- Hoàn thành tầng Ingestion Layer của hệ thống Data Lakehouse.
- Thiết lập thành công hai pipeline tiếp nhận dữ liệu theo mô hình Batch và Streaming.
- Dữ liệu được ghi tự động vào Amazon S3 thông qua API Gateway, Lambda và Kinesis Data Firehose.
- Xây dựng được cơ chế đồng bộ dữ liệu theo lịch bằng Amazon EventBridge Scheduler.
- Kiểm tra thành công quá trình tiếp nhận dữ liệu và sẵn sàng triển khai các bước xử lý ETL ở tầng Bronze trong tuần tiếp theo.