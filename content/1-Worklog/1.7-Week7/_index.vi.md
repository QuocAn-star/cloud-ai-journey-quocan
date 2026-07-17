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

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Xây dựng AWS Glue ETL Job để tổng hợp dữ liệu từ Silver Layer, thực hiện các phép tính thống kê và tạo các bảng dữ liệu phục vụ phân tích như doanh thu theo ngày, doanh thu theo quốc gia, phương thức thanh toán, thiết bị truy cập và các chỉ số tổng hợp khác. | 01/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |
| **3** | Lưu kết quả xử lý vào Gold Layer trên Amazon S3 theo định dạng Parquet, đồng thời kiểm tra cấu trúc dữ liệu và đánh giá tính chính xác của các bảng dữ liệu tổng hợp trước khi phục vụ truy vấn. | 02/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **4** | Thiết lập AWS Glue Data Catalog, tạo cơ sở dữ liệu và đăng ký các bảng trong Gold Layer nhằm quản lý metadata và cung cấp nguồn dữ liệu cho các dịch vụ phân tích trên AWS. | 03/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html |
| **5** | Kiểm tra thông tin metadata của các bảng trong AWS Glue Data Catalog, xác nhận kiểu dữ liệu, cấu trúc bảng và khả năng truy cập nhằm đảm bảo dữ liệu sẵn sàng cho việc truy vấn bằng Amazon Athena. | 04/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/populate-data-catalog.html |
| **6** | Hoàn thiện quy trình chuyển đổi dữ liệu từ Silver Layer đến Gold Layer, đánh giá kết quả xử lý và chuẩn bị môi trường dữ liệu cho giai đoạn xây dựng các truy vấn phân tích bằng Amazon Athena. | 05/06/2026 | AWS Document |


## Kết quả đạt được

- Hoàn thành quy trình chuyển đổi dữ liệu từ Silver Layer sang Gold Layer bằng AWS Glue.
- Xây dựng thành công các bảng dữ liệu tổng hợp phục vụ phân tích và trực quan hóa.
- Tạo và quản lý cơ sở dữ liệu cùng các bảng trong AWS Glue Data Catalog.
- Đảm bảo dữ liệu trong Gold Layer sẵn sàng để truy vấn bằng Amazon Athena.
- Hoàn thiện tầng dữ liệu cuối cùng của kiến trúc Medallion Data Lakehouse.