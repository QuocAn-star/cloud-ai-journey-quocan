---
title: "Worklog Tuần 9"
date: 2026-06-22
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
---

**Thời gian:** 22/06/2026 - 28/06/2026

## Mục tiêu tuần 9

- Triển khai Dashboard lên Amazon EC2 để có thể truy cập từ Internet.
- Cấu hình môi trường thực thi cho ứng dụng Streamlit.
- Kết nối Dashboard với Amazon Athena trên môi trường AWS.
- Kiểm tra toàn bộ quá trình triển khai và đảm bảo hệ thống hoạt động ổn định.

## Công việc đã thực hiện

- Khởi tạo Amazon EC2 để triển khai ứng dụng Dashboard.
- Cấu hình các thành phần mạng bao gồm:
  - VPC.
  - Public Subnet.
  - Internet Gateway.
  - Route Table.
  - Security Group.
- Thiết lập kết nối SSH từ máy cá nhân đến Amazon EC2 bằng khóa bảo mật (.pem).
- Cài đặt môi trường Python và tạo Virtual Environment trên EC2.
- Cài đặt các thư viện phục vụ Dashboard:
  - Streamlit.
  - Pandas.
  - Plotly.
  - AWS Wrangler.
  - Boto3.
  - PyArrow.
- Cấu hình AWS CLI và AWS Credentials trên EC2 để truy cập các dịch vụ AWS.
- Kết nối Dashboard với Amazon Athena và AWS Glue Data Catalog.
- Xử lý các lỗi trong quá trình triển khai như:
  - NoRegionError.
  - NoCredentialsError.
  - Security Group.
  - Public IP.
- Triển khai Dashboard thành công và cấu hình chạy nền bằng `nohup`.
- Kiểm tra khả năng truy cập Dashboard thông qua Public IPv4 của Amazon EC2.

## Kết quả đạt được

- Triển khai thành công Dashboard lên Amazon EC2.
- Dashboard có thể truy cập từ Internet thông qua Public IP.
- Kết nối ổn định với Amazon Athena và AWS Glue Data Catalog.
- Hoàn thành môi trường triển khai cho hệ thống Customer Behavior Analytics trên AWS.
- Sẵn sàng tích hợp toàn bộ pipeline và kiểm thử hệ thống trong tuần tiếp theo.