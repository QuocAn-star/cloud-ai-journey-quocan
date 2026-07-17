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

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu AWS Glue ETL và xây dựng Glue Job đầu tiên để đọc dữ liệu từ Bronze Layer trên Amazon S3, đồng thời nghiên cứu quy trình chuyển đổi dữ liệu giữa các tầng trong kiến trúc Data Lakehouse. | 25/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |
| **3** | Thực hiện làm sạch dữ liệu bằng AWS Glue ETL, xử lý các giá trị thiếu, chuẩn hóa tên cột, định dạng dữ liệu và loại bỏ các bản ghi không hợp lệ nhằm nâng cao chất lượng dữ liệu trước khi phân tích. | 26/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html |
| **4** | Chuyển đổi dữ liệu sang định dạng Parquet và lưu kết quả vào Silver Layer trên Amazon S3 để tối ưu dung lượng lưu trữ cũng như cải thiện hiệu suất truy vấn trong các bước xử lý tiếp theo. | 27/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **5** | Kiểm tra dữ liệu sau quá trình chuyển đổi, đối chiếu với dữ liệu nguồn để đánh giá tính đầy đủ và chính xác, đồng thời xác nhận dữ liệu trong Silver Layer đáp ứng yêu cầu cho giai đoạn tổng hợp dữ liệu. | 28/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-glue-job-cloudwatch-metrics.html |
| **6** | Hoàn thiện quy trình AWS Glue ETL từ Bronze Layer đến Silver Layer, tối ưu cấu hình của Glue Job và chuẩn bị dữ liệu cho quá trình xây dựng Gold Layer trong tuần tiếp theo. | 29/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/populate-with-cloudformation-templates.html |


## Kết quả đạt được

- Hiểu được quy trình ETL và cách sử dụng AWS Glue để xử lý dữ liệu.
- Hoàn thành AWS Glue Job cho quá trình chuyển đổi dữ liệu từ Bronze Layer sang Silver Layer.
- Làm sạch và chuẩn hóa dữ liệu thành công, đảm bảo dữ liệu có chất lượng cao cho các bước xử lý tiếp theo.
- Lưu dữ liệu vào Silver Layer theo đúng kiến trúc Medallion Data Lakehouse.
- Kiểm thử thành công quy trình ETL và xác nhận dữ liệu đã được xử lý chính xác.