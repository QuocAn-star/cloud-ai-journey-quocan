---
title: "Worklog Tuần 7"
date: 2026-06-01
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
---

**Thời gian:** 01/06/2026 - 06/06/2026

## Mục tiêu tuần 7

- Thiết lập môi trường truy vấn dữ liệu bằng Amazon Athena.
- Kiểm tra tính chính xác của các bảng dữ liệu trong AWS Glue Data Catalog.
- Thực hiện truy vấn và xác thực dữ liệu tại Gold Layer.
- Chuẩn bị nguồn dữ liệu phục vụ xây dựng Dashboard.

## Công việc đã thực hiện

- Cấu hình Amazon Athena để truy vấn dữ liệu từ AWS Glue Data Catalog.
- Thiết lập thư mục lưu kết quả truy vấn (Athena Query Results) trên Amazon S3.
- Kiểm tra các bảng đã đăng ký trong Glue Data Catalog, bao gồm:
  - Dashboard Summary.
  - Daily Revenue.
  - Event Summary.
  - Country Revenue.
  - Device Summary.
  - Payment Summary.
  - Source Summary.
- Thực hiện các câu lệnh SQL để xác minh dữ liệu tại Gold Layer.
- Đối chiếu kết quả truy vấn với dữ liệu đã xử lý trong Gold Layer nhằm đảm bảo tính chính xác.
- Kiểm tra hiệu suất truy vấn và xác nhận Amazon Athena có thể đọc trực tiếp dữ liệu định dạng Apache Parquet.
- Hoàn thiện kết nối giữa Gold Layer và Amazon Athena để phục vụ trực quan hóa dữ liệu.

## Kết quả đạt được

- Cấu hình thành công Amazon Athena và AWS Glue Data Catalog.
- Truy vấn thành công các bảng dữ liệu trong Gold Layer.
- Xác nhận dữ liệu phân tích đã sẵn sàng phục vụ Dashboard.
- Hoàn thiện tầng Query Layer trong kiến trúc Data Lakehouse.
- Chuẩn bị đầy đủ dữ liệu để phát triển Dashboard trong tuần tiếp theo.