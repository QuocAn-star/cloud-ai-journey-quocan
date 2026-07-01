---
title: "Ngày 2"
date: 2026-04-21
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

> **Ngày 2 - Compute, Networking và Storage trên AWS:** Tìm hiểu AWS CLI, Amazon EC2, Amazon VPC, Amazon CloudFront, AWS Lambda, AWS CDK và quản lý lưu trữ với Amazon S3.

---

## Mục tiêu trong ngày

- Thành thạo cách quản lý tài nguyên AWS bằng **AWS Command Line Interface (AWS CLI)**.
- Hiểu các khái niệm nền tảng về **Amazon VPC** và hệ thống mạng trên AWS.
- Thực hành triển khai một web server trên **Amazon EC2** trong VPC tùy chỉnh.
- Khám phá **Amazon CloudFront** và **Lambda@Edge** để tối ưu hiệu suất phân phối nội dung.
- Hiểu mô hình điện toán serverless với **AWS Lambda**.
- Làm quen với **Infrastructure as Code** thông qua AWS CDK.
- Tìm hiểu cách quản lý vòng đời dữ liệu với **Amazon S3 Lifecycle Policies** và tự động hóa snapshot bằng **Amazon EBS Data Lifecycle Manager**.

---

# AWS Command Line Interface (AWS CLI)

Nội dung đầu tiên trong ngày là tìm hiểu **AWS CLI**, công cụ dòng lệnh thống nhất giúp quản lý toàn bộ dịch vụ AWS mà không cần sử dụng AWS Console.

Thay vì thao tác trực tiếp trên giao diện web, AWS CLI cho phép tạo, quản lý và tự động hóa hạ tầng thông qua các câu lệnh trong Terminal.

Các nội dung đã thực hành gồm:

- Cài đặt và cấu hình AWS CLI bằng `aws configure`.
- Quản lý nhiều tài khoản thông qua Named Profiles.
- Thực hiện các câu lệnh phổ biến như:
  - `aws s3 ls`
  - `aws ec2 describe-instances`
  - `aws iam list-users`
- Lọc kết quả bằng **JMESPath** với tham số `--query`.
- Xuất kết quả dưới các định dạng JSON, Table và Text.

AWS CLI là nền tảng quan trọng cho việc tự động hóa hạ tầng và các quy trình DevOps trên AWS.

---

# Thực hành triển khai Web Server trên Amazon EC2

Hoạt động thực hành chính trong ngày là xây dựng và triển khai một web server hoàn chỉnh trong môi trường mạng tùy chỉnh.

## Xây dựng Amazon VPC

Thay vì sử dụng VPC mặc định, toàn bộ hạ tầng mạng được tạo mới từ đầu.

Kiến trúc bao gồm:

- Một Virtual Private Cloud (VPC)
- Một Public Subnet
- Internet Gateway
- Route Table
- Security Group

Thông qua bài thực hành này có thể hiểu rõ cách các thành phần mạng trên AWS phối hợp để cung cấp kết nối Internet cho tài nguyên bên trong VPC.

---

## Khởi tạo Amazon EC2 Instance

Sau khi hoàn tất phần networking, tiến hành khởi tạo một EC2 Instance.

Cấu hình bao gồm:

- Amazon Linux AMI
- Instance loại t2.micro
- Đặt trong Public Subnet
- Mở cổng HTTP và SSH trong Security Group

Đồng thời sử dụng **User Data Script** để tự động cài đặt Apache Web Server ngay khi máy chủ khởi động.

Sau khi hoàn thành, website có thể truy cập trực tiếp thông qua Public IP của EC2 Instance.

Bài thực hành này giúp hình dung đầy đủ quy trình triển khai một ứng dụng web trên AWS.

---

# Amazon CloudFront và Lambda@Edge

Tiếp theo là tìm hiểu cách AWS tối ưu hiệu suất phân phối nội dung trên phạm vi toàn cầu.

## Amazon CloudFront

Amazon CloudFront là dịch vụ **Content Delivery Network (CDN)** của AWS, giúp lưu trữ nội dung tại các Edge Locations trên toàn thế giới nhằm giảm độ trễ khi người dùng truy cập.

Các khái niệm chính bao gồm:

- CloudFront Distribution
- Origin
- Behavior
- Cache Policy
- HTTPS
- Edge Locations

CloudFront giúp tăng tốc độ tải website và giảm tải cho máy chủ gốc.

---

## Lambda@Edge

Lambda@Edge mở rộng khả năng của AWS Lambda bằng cách cho phép thực thi mã tại các Edge Locations của CloudFront.

Một số trường hợp sử dụng phổ biến:

- Viết lại URL
- Xác thực người dùng
- Thay đổi Header
- Tối ưu hình ảnh
- A/B Testing

Việc xử lý gần người dùng hơn giúp giảm đáng kể độ trễ mà không cần thay đổi backend.

---

# AWS Lambda

Tiếp theo là tìm hiểu **AWS Lambda**, dịch vụ điện toán serverless của AWS.

Thay vì quản lý máy chủ, người phát triển chỉ cần triển khai mã nguồn, còn AWS sẽ tự động đảm nhận:

- Quản lý hạ tầng
- Tự động mở rộng
- Đảm bảo tính sẵn sàng
- Bảo trì hệ điều hành

Các khái niệm quan trọng được tìm hiểu gồm:

- Event-driven Architecture
- Lambda Function
- Handler
- Trigger
- Concurrency
- Lambda Layers
- Environment Variables
- Lambda Function URL

AWS Lambda tính phí dựa trên số lượng request và thời gian thực thi, giúp tối ưu chi phí cho các ứng dụng có lưu lượng không ổn định.

---

# Infrastructure as Code với AWS CDK

Sau khi tìm hiểu về Serverless, nội dung tiếp theo là **AWS Cloud Development Kit (AWS CDK)**.

AWS CDK cho phép xây dựng hạ tầng bằng các ngôn ngữ lập trình quen thuộc thay vì viết trực tiếp CloudFormation Template.

Các khái niệm được tìm hiểu gồm:

- Constructs
- Stack
- Application
- L1, L2 và L3 Constructs

Quy trình triển khai cơ bản:

```bash
cdk init
cdk synth
cdk deploy
cdk destroy
```

So với CloudFormation thuần, AWS CDK mang lại nhiều lợi ích:

- Kiểm tra kiểu dữ liệu (Type Safety)
- Hỗ trợ Auto-complete trong IDE
- Có thể tái sử dụng thành phần
- Quản lý hạ tầng theo mô hình phát triển phần mềm

Điều này giúp Infrastructure as Code trở nên trực quan và dễ bảo trì hơn.

---

# AWS Toolkit for Visual Studio Code

Để hỗ trợ quá trình phát triển, AWS Toolkit for VS Code cũng được giới thiệu.

Extension này cho phép tương tác trực tiếp với các dịch vụ AWS ngay trong Visual Studio Code.

Các chức năng đã tìm hiểu gồm:

- Quản lý Lambda Functions
- Xem CloudWatch Logs
- Quản lý đối tượng trên Amazon S3
- Chạy và Debug Lambda ngay trên máy cục bộ
- Quản lý AWS Credentials và Profiles

AWS Toolkit giúp giảm đáng kể thời gian chuyển đổi giữa IDE và AWS Console.

---

# Amazon S3 Lifecycle Policies

Một nội dung quan trọng khác là tối ưu hóa lưu trữ trên Amazon S3.

**S3 Lifecycle Policies** cho phép tự động chuyển đổi dữ liệu giữa các lớp lưu trữ theo thời gian.

Ví dụ:

| Hành động | Thời điểm |
|-----------|-----------|
| Chuyển sang S3 Standard-IA | Sau 30 ngày |
| Chuyển sang Glacier Instant Retrieval | Sau 90 ngày |
| Xóa dữ liệu | Sau 365 ngày |

Lifecycle Policies giúp giảm đáng kể chi phí lưu trữ mà không cần quản lý thủ công.

---

# Amazon EBS Data Lifecycle Manager

Phần cuối cùng trong ngày là **Amazon EBS Data Lifecycle Manager (DLM)**.

DLM cho phép tự động hóa:

- Lịch tạo Snapshot
- Chính sách lưu giữ Snapshot
- Sao chép Snapshot giữa các Region
- Quản lý vòng đời Backup

Việc tự động hóa Snapshot giúp đảm bảo dữ liệu luôn được sao lưu đầy đủ đồng thời giảm công sức quản trị.

---

# Bài học rút ra

- Thành thạo cách sử dụng AWS CLI để quản lý và tự động hóa tài nguyên AWS.
- Xây dựng thành công môi trường mạng với Amazon VPC và triển khai Web Server trên Amazon EC2.
- Hiểu cách Amazon CloudFront tăng tốc phân phối nội dung và Lambda@Edge xử lý dữ liệu tại các Edge Locations.
- Nắm được mô hình điện toán Serverless với AWS Lambda.
- Làm quen với Infrastructure as Code thông qua AWS CDK và AWS Toolkit for VS Code.
- Biết cách tối ưu chi phí lưu trữ bằng Amazon S3 Lifecycle Policies.
- Tự động hóa quá trình sao lưu dữ liệu với Amazon EBS Data Lifecycle Manager.

---

*Nguồn tài liệu chính: https://cloudjourney.awsstudygroup.com/*