---
title: "Worklog Tuần 8"
date: 2026-06-08
weight: 8
chapter: false
pre: " <b> 1.8. </b> "
---

**Thời gian:** 08/06/2026 - 14/06/2026

## Mục tiêu tuần 8

- Xây dựng Dashboard trực quan hóa dữ liệu bằng Streamlit.
- Kết nối Dashboard với Amazon Athena để truy vấn dữ liệu trực tiếp từ Gold Layer.
- Thiết kế giao diện hiển thị các chỉ số KPI và biểu đồ phân tích.
- Kiểm tra tính chính xác của dữ liệu hiển thị trên Dashboard.

## Công việc đã thực hiện

- Xây dựng Dashboard bằng **Streamlit** để trực quan hóa dữ liệu phân tích.
- Tích hợp thư viện **AWS Wrangler (awswrangler)** nhằm kết nối Dashboard với Amazon Athena.
- Thiết lập cơ chế truy vấn dữ liệu trực tiếp từ các bảng trong AWS Glue Data Catalog.
- Thiết kế giao diện Dashboard bao gồm:
  - Tổng số đơn hàng.
  - Tổng số khách hàng.
  - Tổng doanh thu.
  - Giá trị đơn hàng trung bình.
  - Tổng số sự kiện.
- Xây dựng các biểu đồ phân tích:
  - Doanh thu theo thời gian.
  - Phân bố sự kiện người dùng.
  - Doanh thu theo quốc gia.
  - Doanh thu theo thiết bị.
  - Doanh thu theo phương thức thanh toán.
  - Doanh thu theo nguồn truy cập.
- Kiểm tra tính chính xác giữa dữ liệu hiển thị trên Dashboard và kết quả truy vấn từ Amazon Athena.
- Tối ưu giao diện để hỗ trợ trực quan hóa dữ liệu và nâng cao trải nghiệm người dùng.

## Kết quả đạt được

- Hoàn thành Dashboard phân tích dữ liệu bằng Streamlit.
- Kết nối thành công Dashboard với Amazon Athena và AWS Glue Data Catalog.
- Hiển thị đầy đủ các chỉ số KPI và biểu đồ phân tích từ Gold Layer.
- Xác nhận dữ liệu hiển thị trên Dashboard chính xác với dữ liệu lưu trữ trong hệ thống.
- Chuẩn bị Dashboard sẵn sàng cho quá trình triển khai lên Amazon EC2 ở tuần tiếp theo.