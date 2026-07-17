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

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
|:---:|-----------|:------------:|:---------------:|----------------|
| **2** | - Tạo Amazon EC2 Instance.<br>- Cấu hình Security Group, Key Pair và các thiết lập mạng cơ bản.<br>- Kết nối đến EC2 thông qua SSH. | 22/06/2026 | 22/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html |
| **3** | - Cài đặt Python và các thư viện cần thiết trên EC2.<br>- Upload mã nguồn Dashboard lên máy chủ.<br>- Cấu hình môi trường thực thi ứng dụng. | 23/06/2026 | 23/06/2026 | https://docs.streamlit.io/deploy/tutorials |
| **4** | - Cấu hình kết nối giữa Dashboard và Amazon Athena.<br>- Kiểm tra khả năng truy vấn dữ liệu từ EC2.<br>- Khắc phục các lỗi cấu hình nếu có. | 24/06/2026 | 24/06/2026 | https://aws-sdk-pandas.readthedocs.io/en/stable/ |
| **5** | - Triển khai ứng dụng Streamlit trên EC2.<br>- Kiểm tra khả năng truy cập Dashboard thông qua địa chỉ IP công khai.<br>- Đánh giá hiệu năng của ứng dụng. | 25/06/2026 | 25/06/2026 | https://docs.streamlit.io/develop/concepts |
| **6** | - Kiểm thử toàn bộ hệ thống sau khi triển khai.<br>- Đánh giá tính ổn định của Dashboard và khả năng truy cập dữ liệu.<br>- Hoàn thiện môi trường triển khai. | 26/06/2026 | 26/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html |

## Kết quả đạt được

- Hoàn thành triển khai Dashboard trên Amazon EC2.
- Cấu hình thành công môi trường thực thi và kết nối với các dịch vụ AWS.
- Dashboard có thể truy cập thông qua địa chỉ IP công khai và hiển thị dữ liệu chính xác.
- Kiểm thử thành công quá trình truy vấn dữ liệu từ Amazon Athena.
- Hoàn thiện môi trường triển khai, sẵn sàng cho giai đoạn kiểm thử và tối ưu hệ thống.