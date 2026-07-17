---
title: "Worklog Tuần 7"
date: 2026-06-01
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
---

**Thời gian:** 01/06/2026 - 05/06/2026

## Mục tiêu tuần 7

- Hoàn thiện quá trình xử lý dữ liệu từ Silver Layer sang Gold Layer.
- Xây dựng các bảng dữ liệu tổng hợp phục vụ phân tích hành vi khách hàng.
- Tạo và quản lý Metadata bằng AWS Glue Data Catalog.
- Chuẩn bị dữ liệu cho việc truy vấn bằng Amazon Athena.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
|:---:|-----------|:------------:|:---------------:|----------------|
| **2** | - Thiết kế các bảng dữ liệu tổng hợp (Gold Layer).<br>- Xác định các chỉ số cần phân tích như doanh thu, phương thức thanh toán, thiết bị và nguồn truy cập. | 01/06/2026 | 01/06/2026 | AWS Document |
| **3** | - Xây dựng AWS Glue Job để chuyển dữ liệu từ Silver Layer sang Gold Layer.<br>- Thực hiện tổng hợp dữ liệu theo yêu cầu phân tích. | 02/06/2026 | 02/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/add-job.html |
| **4** | - Lưu dữ liệu tổng hợp vào Gold Layer trên Amazon S3.<br>- Kiểm tra tính chính xác và đầy đủ của dữ liệu sau khi xử lý. | 03/06/2026 | 03/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **5** | - Tạo AWS Glue Data Catalog Database.<br>- Đăng ký các bảng dữ liệu trong Glue Data Catalog để phục vụ truy vấn. | 04/06/2026 | 04/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html |
| **6** | - Kiểm tra các bảng dữ liệu trong Glue Data Catalog.<br>- Đánh giá cấu trúc dữ liệu và chuẩn bị cho việc truy vấn bằng Amazon Athena. | 05/06/2026 | 05/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/data-sources-glue.html |

## Kết quả đạt được

- Hoàn thành quy trình chuyển đổi dữ liệu từ Silver Layer sang Gold Layer bằng AWS Glue.
- Xây dựng thành công các bảng dữ liệu tổng hợp phục vụ phân tích và trực quan hóa.
- Tạo và quản lý cơ sở dữ liệu cùng các bảng trong AWS Glue Data Catalog.
- Đảm bảo dữ liệu trong Gold Layer sẵn sàng để truy vấn bằng Amazon Athena.
- Hoàn thiện tầng dữ liệu cuối cùng của kiến trúc Medallion Data Lakehouse.