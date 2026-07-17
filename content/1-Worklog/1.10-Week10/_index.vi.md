---
title: "Worklog Tuần 10"
date: 2026-06-15
weight: 10
chapter: false
pre: " <b> 1.10. </b> "
---

**Thời gian:** 22/06/2026 - 26/06/2026

## Mục tiêu tuần 10

- Triển khai Dashboard lên máy chủ Amazon EC2.
- Cấu hình môi trường chạy ứng dụng và kết nối với các dịch vụ AWS.
- Kiểm thử khả năng truy cập Dashboard từ bên ngoài.
- Đánh giá hiệu năng và tính ổn định của hệ thống sau khi triển khai.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Khởi tạo một Amazon EC2 Instance, cấu hình Key Pair, Security Group và các thiết lập mạng cần thiết, sau đó kết nối đến máy chủ thông qua SSH để chuẩn bị môi trường triển khai ứng dụng. | 22/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html |
| **3** | Cài đặt Python và các thư viện cần thiết trên Amazon EC2, sao chép mã nguồn Dashboard lên máy chủ, đồng thời cấu hình môi trường thực thi để ứng dụng có thể kết nối với các dịch vụ AWS. | 23/06/2026 | https://docs.streamlit.io/deploy/tutorials |
| **4** | Cấu hình ứng dụng Streamlit kết nối với Amazon Athena và AWS Glue Data Catalog, kiểm tra khả năng truy vấn dữ liệu từ EC2 và xử lý các lỗi cấu hình phát sinh trong quá trình triển khai. | 24/06/2026 | https://aws-sdk-pandas.readthedocs.io/en/stable/ |
| **5** | Triển khai ứng dụng Streamlit trên Amazon EC2, cấu hình cổng truy cập và kiểm tra Dashboard thông qua địa chỉ IP công khai nhằm đảm bảo người dùng có thể truy cập và sử dụng hệ thống từ bên ngoài. | 25/06/2026 | https://docs.streamlit.io/develop/concepts |
| **6** | Kiểm thử toàn bộ quá trình triển khai, đánh giá hiệu năng truy cập Dashboard, xác nhận khả năng truy vấn dữ liệu từ Amazon Athena và hoàn thiện môi trường triển khai cho hệ thống. | 26/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html |

## Kết quả đạt được

- Hoàn thành triển khai Dashboard trên Amazon EC2.
- Cấu hình thành công môi trường thực thi và kết nối với các dịch vụ AWS.
- Dashboard có thể truy cập thông qua địa chỉ IP công khai và hiển thị dữ liệu chính xác.
- Kiểm thử thành công quá trình truy vấn dữ liệu từ Amazon Athena.
- Hoàn thiện môi trường triển khai, sẵn sàng cho giai đoạn kiểm thử và tối ưu hệ thống.