---
title: "Worklog Tuần 10"
date: 2026-06-15
weight: 10
chapter: false
pre: " <b> 1.10. </b> "
---

**Thời gian:** 15/06/2026 - 21/06/2026

## Mục tiêu tuần 10

- Tích hợp toàn bộ các thành phần của hệ thống Data Lakehouse.
- Kiểm thử luồng xử lý dữ liệu từ Data Source đến Dashboard.
- Đánh giá tính ổn định và độ chính xác của hệ thống.
- Hoàn thiện kiến trúc End-to-End trước khi tối ưu và hoàn thiện báo cáo.

## Công việc đã thực hiện

- Tích hợp toàn bộ pipeline xử lý dữ liệu bao gồm:
  - Batch Processing.
  - Streaming Processing.
  - AWS Glue ETL.
  - AWS Glue Data Catalog.
  - Amazon Athena.
  - Streamlit Dashboard.
- Kiểm tra luồng dữ liệu từ nguồn dữ liệu đến Dashboard:
  - Data Source.
  - Raw Layer.
  - Bronze Layer.
  - Silver Layer.
  - Gold Layer.
  - Athena.
  - Dashboard.
- Thực hiện nhiều lần chạy thử quy trình ETL nhằm kiểm tra tính ổn định của hệ thống.
- Kiểm tra dữ liệu tại từng tầng để đảm bảo dữ liệu được xử lý chính xác.
- Đối chiếu kết quả truy vấn trên Amazon Athena với dữ liệu hiển thị trên Dashboard.
- Kiểm tra khả năng cập nhật dữ liệu khi có dữ liệu mới từ cả Batch Processing và Streaming Processing.
- Hoàn thiện sơ đồ kiến trúc tổng thể của hệ thống để phục vụ báo cáo và thuyết trình.

## Kết quả đạt được

- Hoàn thành việc tích hợp toàn bộ kiến trúc Data Lakehouse.
- Xác nhận dữ liệu được xử lý xuyên suốt từ nguồn dữ liệu đến Dashboard.
- Kiểm chứng tính chính xác giữa dữ liệu trong Amazon Athena và Dashboard.
- Đảm bảo hệ thống hoạt động ổn định đối với cả Batch Processing và Streaming Processing.
- Hoàn thiện phiên bản End-to-End của hệ thống Customer Behavior Analytics trên nền tảng AWS.