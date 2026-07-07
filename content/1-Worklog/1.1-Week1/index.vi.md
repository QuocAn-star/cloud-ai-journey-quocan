---
title: "Worklog Tuần 1"
date: 2026-04-20
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

**Thời gian:** 20/04/2026 - 26/04/2026

## Mục tiêu tuần 1

- Làm quen với chương trình thực tập và yêu cầu triển khai báo cáo theo FCAJ Workshop Template.
- Nghiên cứu bài toán **Customer Behavior Analytics** và các yêu cầu phân tích dữ liệu từ hệ thống thương mại điện tử.
- Tìm hiểu kiến trúc **Medallion Data Lakehouse** trên AWS và các dịch vụ sẽ sử dụng trong dự án.
- Xây dựng định hướng tổng thể cho pipeline xử lý dữ liệu theo mô hình Batch và Streaming.

## Công việc đã thực hiện

- Tìm hiểu cấu trúc báo cáo thực tập bằng Hugo Workshop Template và các thành phần cần hoàn thành trong suốt quá trình thực tập.
- Khảo sát yêu cầu của bài toán Customer Behavior Analytics, bao gồm:
  - Phân tích doanh thu theo thời gian.
  - Phân tích hành vi khách hàng.
  - Thống kê phương thức thanh toán.
  - Phân tích thiết bị và nguồn truy cập.
  - Tổng hợp các chỉ số phục vụ Dashboard.
- Nghiên cứu kiến trúc **Medallion Data Lakehouse** với ba tầng dữ liệu:
  - Bronze Layer.
  - Silver Layer.
  - Gold Layer.
- Tìm hiểu vai trò của các dịch vụ AWS dự kiến sử dụng trong hệ thống:
  - Amazon S3.
  - AWS Lambda.
  - Amazon API Gateway.
  - Amazon Kinesis Data Firehose.
  - AWS Glue ETL.
  - AWS Glue Data Catalog.
  - Amazon Athena.
  - Amazon EC2.
  - Amazon EventBridge.
  - Amazon CloudWatch.
- Xây dựng ý tưởng tổng thể cho hệ thống xử lý dữ liệu gồm hai luồng:
  - Batch Processing.
  - Streaming Processing.
- Phác thảo kiến trúc Data Lakehouse và xác định luồng dữ liệu từ Data Source đến Dashboard.

## Kết quả đạt được

- Hiểu được yêu cầu của chương trình thực tập và cấu trúc báo cáo theo FCAJ Workshop Template.
- Xác định được mục tiêu của dự án là xây dựng hệ thống **Customer Behavior Analytics** trên nền tảng AWS Data Lakehouse.
- Nắm được vai trò của từng dịch vụ AWS trong toàn bộ pipeline xử lý dữ liệu.
- Hoàn thành định hướng kiến trúc tổng thể theo mô hình **Serverless Medallion Data Lakehouse**, làm cơ sở cho các giai đoạn triển khai ở những tuần tiếp theo.