---
title: "Worklog Tuần 3"
date: 2026-05-03
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
---

**Thời gian:** 04/05/2026 - 08/05/2026

## Mục tiêu tuần 3

- Tìm hiểu các khái niệm cơ bản về mạng trên nền tảng AWS.
- Hiểu vai trò của Amazon VPC trong việc xây dựng hạ tầng mạng an toàn và linh hoạt.
- Thực hành tạo và cấu hình Virtual Private Cloud (VPC) cùng các thành phần liên quan.
- Nắm được cách kiểm soát lưu lượng mạng và bảo mật tài nguyên trên AWS.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu tổng quan về Amazon Virtual Private Cloud (Amazon VPC), nghiên cứu vai trò của VPC trong việc xây dựng hạ tầng mạng riêng trên AWS và tìm hiểu cách các tài nguyên có thể giao tiếp với nhau trong cùng một hệ thống. | 04/05/2026 | https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html |
| **3** | Nghiên cứu kiến trúc mạng trong Amazon VPC, tìm hiểu Public Subnet và Private Subnet, đồng thời thực hành thiết kế mạng để phân tách các thành phần của hệ thống theo từng vùng mạng phù hợp. | 05/05/2026 | https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html |
| **4** | Tìm hiểu Route Table và Internet Gateway, nghiên cứu cơ chế định tuyến lưu lượng mạng giữa các Subnet và Internet nhằm đảm bảo các tài nguyên có thể truy cập hoặc được cô lập theo yêu cầu của hệ thống. | 06/05/2026 | https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html |
| **5** | Nghiên cứu Security Group, tìm hiểu cách thiết lập các quy tắc Inbound và Outbound để kiểm soát lưu lượng truy cập đến các tài nguyên AWS, đồng thời thực hành cấu hình bảo mật cho Amazon EC2. | 07/05/2026 | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html |
| **6** | Tìm hiểu Network Access Control List (Network ACL), nghiên cứu sự khác biệt giữa Security Group và Network ACL, đồng thời thực hành cấu hình nhằm tăng cường khả năng bảo mật cho hạ tầng mạng trên AWS. | 08/05/2026 | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html |


## Kết quả đạt được

- Hiểu được kiến trúc mạng cơ bản trên nền tảng AWS và vai trò của Amazon VPC.
- Hoàn thành việc tạo VPC, Subnet, Internet Gateway và Route Table.
- Cấu hình thành công Security Group và Network ACL để kiểm soát truy cập mạng.
- Thực hành triển khai môi trường mạng cho EC2 và kiểm tra khả năng kết nối.
- Nắm được các nguyên tắc thiết kế và bảo mật mạng trên AWS, tạo nền tảng cho việc triển khai hệ thống Data Lakehouse trong các tuần tiếp theo.