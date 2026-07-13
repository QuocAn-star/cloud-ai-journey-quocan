---
title: "Worklog Tuần 6"
date: 2026-05-25
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
---

**Thời gian:** 25/05/2026 - 31/05/2026

## Mục tiêu tuần 6

- Triển khai Gold Layer trong kiến trúc Medallion Data Lakehouse.
- Xây dựng AWS Glue ETL Job để tổng hợp dữ liệu phục vụ phân tích.
- Tạo các bảng dữ liệu phân tích (Analytical Tables) phục vụ Dashboard.
- Đăng ký các bảng Gold vào AWS Glue Data Catalog để hỗ trợ truy vấn bằng Amazon Athena.

## Công việc đã thực hiện

- Phát triển **AWS Glue ETL Job** chuyển đổi dữ liệu từ Silver Layer sang Gold Layer.
- Xây dựng các bảng dữ liệu tổng hợp phục vụ phân tích:
  - Dashboard Summary.
  - Daily Revenue.
  - Event Summary.
  - Country Revenue.
  - Device Summary.
  - Payment Summary.
  - Source Summary.
- Thực hiện các phép tổng hợp dữ liệu:
  - Đếm số lượng đơn hàng.
  - Đếm số lượng khách hàng.
  - Tính tổng doanh thu.
  - Tính giá trị đơn hàng trung bình.
  - Thống kê doanh thu theo quốc gia, thiết bị, phương thức thanh toán và nguồn truy cập.
- Lưu toàn bộ dữ liệu phân tích xuống Gold Layer dưới định dạng Apache Parquet.
- Tự động đăng ký các bảng Gold vào **AWS Glue Data Catalog**.
- Kiểm tra cấu trúc bảng và xác nhận các bảng được tạo thành công trong Glue Catalog.

## Kết quả đạt được

- Hoàn thành AWS Glue ETL Job cho quá trình Silver → Gold.
- Xây dựng thành công các bảng dữ liệu phục vụ phân tích nghiệp vụ.
- Hoàn thiện Gold Layer theo mô hình Medallion Data Lakehouse.
- Đăng ký thành công các bảng vào AWS Glue Data Catalog.
- Chuẩn bị đầy đủ dữ liệu để thực hiện truy vấn bằng Amazon Athena và xây dựng Dashboard trong các tuần tiếp theo.