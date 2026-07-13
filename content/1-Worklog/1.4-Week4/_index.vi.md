---
title: "Worklog Tuần 4"
date: 2026-05-10
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
---

**Thời gian:** 11/05/2026 - 17/05/2026

## Mục tiêu tuần 4

- Triển khai Bronze Layer trong kiến trúc Medallion Data Lakehouse.
- Xây dựng AWS Glue ETL Job đầu tiên để chuyển đổi dữ liệu từ Raw Layer sang Bronze Layer.
- Chuẩn hóa định dạng lưu trữ dữ liệu nhằm tối ưu cho các bước xử lý tiếp theo.
- Kiểm tra tính đầy đủ và chính xác của dữ liệu sau khi xử lý.

## Công việc đã thực hiện

- Xây dựng **AWS Glue ETL Job** để chuyển đổi dữ liệu từ Raw Layer sang Bronze Layer.
- Cấu hình Glue Job đọc dữ liệu CSV từ Amazon S3 Raw Layer.
- Chuyển đổi dữ liệu từ định dạng CSV sang **Apache Parquet** nhằm tối ưu dung lượng lưu trữ và hiệu suất truy vấn.
- Áp dụng cơ chế **Schema Inference** để tự động xác định kiểu dữ liệu của từng cột.
- Tổ chức dữ liệu theo từng thư mục riêng trong Bronze Layer:
  - Customers.
  - Orders.
  - Products.
  - Events.
- Thiết lập chế độ ghi đè (Overwrite) để cập nhật dữ liệu mới sau mỗi lần ETL.
- Kiểm tra dữ liệu đầu ra trên Amazon S3 và xác nhận các file Parquet được tạo thành công.
- Đánh giá chất lượng dữ liệu nhằm đảm bảo dữ liệu sẵn sàng cho giai đoạn xử lý tại Silver Layer.

## Kết quả đạt được

- Hoàn thành AWS Glue ETL Job chuyển đổi dữ liệu từ Raw Layer sang Bronze Layer.
- Chuẩn hóa định dạng lưu trữ bằng Apache Parquet giúp tối ưu hiệu suất lưu trữ và truy vấn.
- Hoàn thiện cấu trúc Bronze Layer theo mô hình Medallion Data Lakehouse.
- Xác nhận toàn bộ dữ liệu nguồn đã được chuyển đổi và lưu trữ thành công trên Amazon S3.
- Hoàn thành nền tảng dữ liệu Bronze, sẵn sàng triển khai các bước làm sạch và chuẩn hóa dữ liệu tại Silver Layer trong tuần tiếp theo.