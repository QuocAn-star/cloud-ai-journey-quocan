---
title: "Worklog Tuần 5"
date: 2026-05-18
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
---

**Thời gian:** 18/05/2026 - 24/05/2026

## Mục tiêu tuần 5

- Triển khai Silver Layer trong kiến trúc Medallion Data Lakehouse.
- Xây dựng AWS Glue ETL Job để làm sạch và chuẩn hóa dữ liệu từ Bronze Layer.
- Chuẩn hóa cấu trúc dữ liệu nhằm phục vụ cho việc tổng hợp dữ liệu ở Gold Layer.
- Kiểm tra chất lượng dữ liệu sau quá trình làm sạch.

## Công việc đã thực hiện

- Phát triển **AWS Glue ETL Job** chuyển đổi dữ liệu từ Bronze Layer sang Silver Layer.
- Thực hiện loại bỏ các bản ghi trùng lặp (Duplicate Records).
- Chuẩn hóa tên cột theo quy ước thống nhất:
  - Chuyển toàn bộ về chữ thường.
  - Thay khoảng trắng và dấu "-" bằng dấu "_".
- Loại bỏ khoảng trắng dư thừa trong các trường dữ liệu dạng chuỗi.
- Chuẩn hóa các trường ngày tháng sang định dạng Timestamp.
- Kiểm tra kiểu dữ liệu của từng cột nhằm đảm bảo tính nhất quán.
- Ghi dữ liệu đã xử lý xuống Silver Layer dưới định dạng Apache Parquet.
- Kiểm tra kết quả ETL và xác nhận dữ liệu được lưu thành công trên Amazon S3.

## Kết quả đạt được

- Hoàn thành AWS Glue ETL Job cho quá trình Bronze → Silver.
- Làm sạch và chuẩn hóa dữ liệu thành công trước khi phục vụ phân tích.
- Đảm bảo dữ liệu có cấu trúc đồng nhất giữa các bảng.
- Hoàn thiện Silver Layer làm nền tảng cho việc xây dựng các bảng phân tích tại Gold Layer.
- Sẵn sàng triển khai các phép tổng hợp dữ liệu và tạo KPI trong tuần tiếp theo.