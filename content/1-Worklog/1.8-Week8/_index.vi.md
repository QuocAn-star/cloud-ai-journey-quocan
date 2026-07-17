---
title: "Worklog Tuần 8"
date: 2026-06-08
weight: 8
chapter: false
pre: " <b> 1.8. </b> "
---

**Thời gian:** 08/06/2026 - 12/06/2026

## Mục tiêu tuần 8

- Tìm hiểu dịch vụ Amazon Athena và cơ chế truy vấn dữ liệu trên Amazon S3.
- Xây dựng cơ sở dữ liệu và các bảng trong Amazon Athena dựa trên AWS Glue Data Catalog.
- Thực hiện các câu lệnh SQL để phân tích dữ liệu hành vi khách hàng.
- Chuẩn bị nguồn dữ liệu phục vụ cho Dashboard trực quan hóa.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu Amazon Athena và cơ chế truy vấn dữ liệu trực tiếp trên Amazon S3 thông qua AWS Glue Data Catalog, đồng thời nghiên cứu cách cấu hình môi trường truy vấn và thiết lập vị trí lưu trữ kết quả trên Amazon S3. | 08/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/what-is.html |
| **3** | Tạo cơ sở dữ liệu và kết nối Amazon Athena với các bảng đã đăng ký trong AWS Glue Data Catalog, sau đó kiểm tra khả năng truy cập và đọc dữ liệu từ Gold Layer để phục vụ phân tích. | 09/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/databases-tables-columns-names.html |
| **4** | Xây dựng các câu lệnh SQL để phân tích dữ liệu như doanh thu theo ngày, doanh thu theo quốc gia, phương thức thanh toán, thiết bị truy cập và các chỉ số liên quan đến hành vi khách hàng nhằm phục vụ Dashboard. | 10/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/querying.html |
| **5** | Kiểm tra kết quả truy vấn, tối ưu các câu lệnh SQL nhằm cải thiện hiệu năng xử lý, đồng thời đánh giá tính chính xác và nhất quán của dữ liệu trước khi kết nối với Dashboard. | 11/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-query-optimization-techniques.html |
| **6** | Hoàn thiện môi trường truy vấn bằng Amazon Athena, kiểm thử toàn bộ các truy vấn phân tích và chuẩn bị nguồn dữ liệu phục vụ cho việc phát triển Dashboard bằng Streamlit trong giai đoạn tiếp theo. | 12/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/troubleshooting-athena.html |


## Kết quả đạt được

- Hiểu được nguyên lý hoạt động của Amazon Athena và khả năng truy vấn dữ liệu trực tiếp trên Amazon S3.
- Hoàn thành việc tạo Database và kết nối với AWS Glue Data Catalog.
- Xây dựng thành công các truy vấn SQL phục vụ phân tích dữ liệu hành vi khách hàng.
- Kiểm tra và xác nhận tính chính xác của dữ liệu truy vấn.
- Chuẩn bị đầy đủ nguồn dữ liệu phục vụ cho việc xây dựng Dashboard ở giai đoạn tiếp theo.