---
title: "Worklog Tuần 6"
date: 2026-05-25
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
---

**Thời gian:** 25/05/2026 - 29/05/2026

## Mục tiêu tuần 6

- Tìm hiểu quy trình ETL trên AWS Glue.
- Xây dựng quá trình xử lý dữ liệu từ Bronze Layer sang Silver Layer.
- Thực hiện làm sạch, chuẩn hóa và chuyển đổi dữ liệu.
- Chuẩn bị dữ liệu chất lượng cao phục vụ cho giai đoạn phân tích và tổng hợp.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
|:---:|-----------|:------------:|:---------------:|----------------|
| **2** | - Tìm hiểu tổng quan về AWS Glue.<br>- Nghiên cứu quy trình ETL và các thành phần của AWS Glue. | 25/05/2026 | 25/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |
| **3** | - Tạo AWS Glue Job.<br>- Kết nối dữ liệu từ Bronze Layer trên Amazon S3.<br>- Thiết lập môi trường xử lý dữ liệu. | 26/05/2026 | 26/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/add-job.html |
| **4** | - Thực hiện làm sạch dữ liệu.<br>- Chuẩn hóa tên cột, kiểu dữ liệu và loại bỏ dữ liệu không hợp lệ.<br>- Chuyển đổi dữ liệu sang định dạng Parquet. | 27/05/2026 | 27/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html |
| **5** | - Ghi dữ liệu đã xử lý vào Silver Layer trên Amazon S3.<br>- Kiểm tra tính chính xác của dữ liệu sau khi chuyển đổi. | 28/05/2026 | 28/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **6** | - Kiểm thử AWS Glue Job.<br>- Đánh giá kết quả xử lý dữ liệu.<br>- Hoàn thiện quy trình ETL từ Bronze sang Silver. | 29/05/2026 | 29/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-glue-job-cloudwatch-metrics.html |

## Kết quả đạt được

- Hiểu được quy trình ETL và cách sử dụng AWS Glue để xử lý dữ liệu.
- Hoàn thành AWS Glue Job cho quá trình chuyển đổi dữ liệu từ Bronze Layer sang Silver Layer.
- Làm sạch và chuẩn hóa dữ liệu thành công, đảm bảo dữ liệu có chất lượng cao cho các bước xử lý tiếp theo.
- Lưu dữ liệu vào Silver Layer theo đúng kiến trúc Medallion Data Lakehouse.
- Kiểm thử thành công quy trình ETL và xác nhận dữ liệu đã được xử lý chính xác.