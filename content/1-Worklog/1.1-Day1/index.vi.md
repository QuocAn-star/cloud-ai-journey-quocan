---
title: "Ngày 1"
date: 2026-04-20
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

> **Ngày 1 - Khởi động hành trình AWS:** Thiết lập tài khoản AWS, tích lũy AWS Credits, xây dựng hệ thống kiểm soát chi phí và tìm hiểu những kiến thức nền tảng về Cloud Computing cũng như các dịch vụ cốt lõi của AWS.

---

## Mục tiêu trong ngày

- Thiết lập tài khoản AWS và nhận **AWS Credits** để phục vụ quá trình học tập.
- Hoàn thành các nhiệm vụ thực hành đầu tiên nhằm làm quen với môi trường AWS.
- Xây dựng hệ thống giám sát và kiểm soát chi phí ngay từ đầu.
- Hiểu các khái niệm nền tảng về Cloud Computing và mô hình hạ tầng AWS.
- Làm quen với các dịch vụ AWS phổ biến như EC2, S3, IAM, Lambda và RDS.

---

# Thực hành: Kích hoạt tài khoản và nhận AWS Credits

Để bắt đầu chương trình First Cloud Journey, bước đầu tiên là kích hoạt tài khoản AWS và nhận các khoản AWS Credits dành cho học viên.

Ban đầu, AWS cấp **100 USD Credits** để thực hành. Sau đó, bằng cách hoàn thành năm nhiệm vụ hướng dẫn trên AWS Console, có thể nhận thêm **100 USD Credits**, nâng tổng số credit lên **200 USD**.

## Task 1 - Launch EC2 Instance

Dịch vụ đầu tiên được trải nghiệm là **Amazon EC2**, dịch vụ máy chủ ảo của AWS.

Các bước thực hiện gồm:

- Khởi tạo một EC2 Instance.
- Tạo Key Pair.
- Cấu hình Security Group.
- Khởi chạy Instance.
- Terminate Instance sau khi hoàn thành để tránh phát sinh chi phí.

Qua bài thực hành này có thể hiểu được quy trình tạo một máy chủ trên nền tảng Cloud cũng như cách AWS quản lý tài nguyên Compute.

---

## Task 2 - Amazon Bedrock Playground

Tiếp theo là trải nghiệm **Amazon Bedrock**, nền tảng AI Generative AI của AWS.

Trong bài thực hành:

- Gửi yêu cầu sử dụng Foundation Models.
- Thử nghiệm Claude 3 Haiku.
- Thực hiện prompt đơn giản.
- Quan sát kết quả trả về.

Qua đó hiểu rằng nhiều dịch vụ AI trên AWS yêu cầu đăng ký quyền sử dụng trước nhằm đảm bảo Responsible AI.

---

## Task 3 - AWS Budgets

Một trong những nhiệm vụ quan trọng nhất là thiết lập **AWS Budgets**.

AWS Budgets cho phép:

- Đặt giới hạn chi phí.
- Gửi email khi vượt ngưỡng.
- Theo dõi mức tiêu thụ AWS Credits.

Đây là bước gần như bắt buộc đối với bất kỳ ai sử dụng AWS Credits.

---

## Task 4 - AWS Lambda

Tiếp tục với **AWS Lambda**, dịch vụ Serverless Compute.

Thực hành bao gồm:

- Tạo Lambda Function.
- Chạy thử Function.
- Quan sát cơ chế thực thi theo sự kiện.
- Xóa Function sau khi hoàn thành.

Qua đó hiểu được cách AWS vận hành mô hình Serverless mà không cần quản lý máy chủ.

---

## Task 5 - Amazon RDS

Bài thực hành cuối cùng là tạo một cơ sở dữ liệu với **Amazon RDS**.

Các bước thực hiện:

- Khởi tạo Aurora PostgreSQL.
- Chờ Database Available.
- Xóa Database đúng thứ tự để tránh lỗi.

Thông qua bài này có thể thấy AWS chịu trách nhiệm quản lý phần lớn công việc của Database Administrator như backup, patching và maintenance.

---

# Thiết lập hệ thống kiểm soát chi phí

Sau khi hoàn thành các bài thực hành đầu tiên, việc tiếp theo là xây dựng hệ thống kiểm soát chi phí.

Việc này đặc biệt quan trọng vì AWS tính phí theo mức sử dụng thực tế (Pay-as-you-go).

## AWS Budgets

Thiết lập ba mức Budget:

| Budget | Ngưỡng |
|---------|---------|
| Monthly Budget | 50 USD |
| Warning Budget | 25 USD |
| Daily Budget | 10 USD |

Hệ thống này giúp phát hiện sớm khi tài nguyên tiêu tốn chi phí bất thường.

---

## CloudWatch Billing Alarm

CloudWatch Billing Alarm được cấu hình theo nhiều mức:

| Mức chi phí | Thông báo |
|-------------|-----------|
| 25 USD | Email |
| 50 USD | Email + SMS |
| 75 USD | Email + SMS + Slack |

Cơ chế cảnh báo nhiều lớp giúp hạn chế tối đa việc vượt ngân sách.

---

## AWS Cost Explorer

Cost Explorer được bật để:

- Theo dõi chi phí hằng ngày.
- Phân tích dịch vụ tiêu tốn nhiều nhất.
- Theo dõi xu hướng sử dụng AWS Credits.

---

## Resource Tagging

Toàn bộ tài nguyên AWS được gắn Tag theo chuẩn:

| Tag | Ý nghĩa |
|------|----------|
| Project | FCAJ |
| Environment | Dev |
| Owner | User |

Tagging giúp việc theo dõi chi phí và quản lý tài nguyên trở nên đơn giản hơn.

---

# Kiến thức nền tảng AWS

Sau khi hoàn thành phần thực hành, tiếp tục tìm hiểu các khái niệm nền tảng của AWS.

## Cloud Computing

Ba lợi ích lớn nhất của Cloud Computing:

- Elasticity
- Pay-as-you-go
- Global Infrastructure

Đây là nền tảng của mọi dịch vụ AWS.

---

## AWS Global Infrastructure

Tìm hiểu mô hình hạ tầng của AWS gồm:

- Regions
- Availability Zones
- Edge Locations

Kiến trúc này giúp AWS đảm bảo tính sẵn sàng cao và khả năng mở rộng trên toàn cầu.

---

## AWS Identity and Access Management (IAM)

IAM là dịch vụ quản lý danh tính và quyền truy cập.

Các thành phần chính gồm:

- Root Account
- IAM Users
- IAM Groups
- IAM Policies
- MFA
- Least Privilege Principle

IAM đóng vai trò là lớp bảo mật đầu tiên của mọi tài khoản AWS.

---

## Tổng quan các dịch vụ AWS

Trong ngày đầu tiên cũng tìm hiểu sơ bộ các dịch vụ phổ biến:

- Amazon EC2
- Amazon S3
- Amazon RDS
- AWS Lambda

Đây là những dịch vụ xuất hiện xuyên suốt trong hầu hết các kiến trúc trên AWS.

---

# Bài học rút ra

- Hoàn thành quá trình khởi tạo tài khoản AWS và nhận tổng cộng **200 USD AWS Credits**.
- Hiểu cách kiểm soát chi phí ngay từ đầu thông qua AWS Budgets, CloudWatch Billing Alarm và Cost Explorer.
- Nắm được các khái niệm nền tảng của Cloud Computing và kiến trúc toàn cầu của AWS.
- Làm quen với các dịch vụ cốt lõi như EC2, S3, IAM, Lambda và RDS.
- Hình thành thói quen **triển khai xong phải dọn dẹp tài nguyên** nhằm tránh phát sinh chi phí không mong muốn.

---

*Nguồn tài liệu chính: https://cloudjourney.awsstudygroup.com/*