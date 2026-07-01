---
title: "Ngày 3"
date: 2026-04-22
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
---

> **Ngày 3 - Infrastructure as Code và Data Engineering trên AWS:** Tìm hiểu AWS CloudFormation, AWS CDK, thực hành kiểm thử hạ tầng bằng Floci và LocalStack, xây dựng data pipeline với AWS Glue và Amazon Athena, đồng thời triển khai cơ sở dữ liệu quan hệ bằng Amazon RDS.

---

## Mục tiêu trong ngày

- Hiểu khái niệm **Infrastructure as Code (IaC)** và lợi ích của việc quản lý hạ tầng bằng mã.
- Làm quen với **AWS CloudFormation** và **AWS CDK**.
- Kiểm thử kiến trúc hạ tầng cục bộ bằng **Floci** và **LocalStack**.
- Xây dựng một data pipeline đơn giản trên AWS.
- Tìm hiểu quy trình ETL với **AWS Glue** và truy vấn dữ liệu bằng **Amazon Athena**.
- Thực hành triển khai cơ sở dữ liệu quan hệ với **Amazon RDS**.

---

# Infrastructure as Code với AWS CloudFormation

Nội dung đầu tiên trong ngày là tìm hiểu **AWS CloudFormation**, dịch vụ Infrastructure as Code (IaC) gốc của AWS.

Thay vì tạo tài nguyên thủ công trên AWS Console, toàn bộ hạ tầng được định nghĩa bằng các template dưới dạng YAML hoặc JSON. Điều này giúp việc triển khai trở nên nhất quán, có thể lặp lại và dễ dàng kiểm soát phiên bản.

Một CloudFormation Template thường bao gồm:

- Parameters
- Resources
- Outputs
- Mappings
- Conditions

Trong đó, **Resources** là thành phần bắt buộc vì định nghĩa toàn bộ tài nguyên AWS sẽ được tạo.

---

## Các khái niệm quan trọng

Một số khái niệm được tìm hiểu bao gồm:

- **Stacks** để quản lý nhiều tài nguyên như một đơn vị duy nhất.
- **Change Sets** nhằm xem trước những thay đổi trước khi triển khai.
- **StackSets** để triển khai cùng một hạ tầng trên nhiều AWS Accounts hoặc Regions.
- **Nested Stacks** giúp chia nhỏ các template lớn.
- **Drift Detection** để phát hiện các thay đổi được thực hiện ngoài CloudFormation.

CloudFormation giúp Infrastructure trở thành một phần của quy trình phát triển phần mềm thay vì được cấu hình thủ công.

---

# Infrastructure as Code với AWS CDK

Sau CloudFormation, tiếp tục tìm hiểu **AWS Cloud Development Kit (AWS CDK)**.

AWS CDK cho phép định nghĩa hạ tầng bằng các ngôn ngữ lập trình quen thuộc như:

- TypeScript
- Python
- Java
- C#
- Go

Thay vì viết trực tiếp CloudFormation Template, CDK sẽ tự động sinh ra CloudFormation phía dưới.

Quy trình làm việc cơ bản gồm:

```bash
cdk init
cdk synth
cdk deploy
cdk destroy
```

Các thành phần chính của CDK gồm:

- Application
- Stack
- Constructs

Đồng thời tìm hiểu ba cấp độ Constructs:

- L1 Constructs
- L2 Constructs
- L3 Constructs

AWS CDK mang lại nhiều lợi ích như hỗ trợ kiểm tra kiểu dữ liệu, gợi ý mã nguồn và tái sử dụng hạ tầng theo mô hình lập trình hướng đối tượng.

---

# Kiểm thử hạ tầng với Floci và LocalStack

Sau khi xây dựng Infrastructure as Code, bước tiếp theo là kiểm thử hạ tầng trước khi triển khai lên AWS.

## Floci

Floci là một AWS Emulator nhẹ, giúp mô phỏng các dịch vụ AWS ngay trên máy cục bộ.

Ưu điểm của Floci:

- Khởi động nhanh.
- Tiêu tốn ít bộ nhớ.
- Hỗ trợ kiểm thử S3, Lambda và DynamoDB.
- Không phát sinh chi phí AWS.

Floci đặc biệt phù hợp trong giai đoạn phát triển ban đầu khi cần xác minh logic của hạ tầng.

---

## LocalStack

Đối với các dịch vụ phức tạp hơn, sử dụng **LocalStack**.

LocalStack hỗ trợ mô phỏng nhiều dịch vụ AWS như:

- Amazon S3
- AWS Lambda
- Amazon Kinesis
- Amazon SNS
- Amazon SQS
- Amazon DynamoDB

Thông qua Docker, toàn bộ môi trường AWS có thể được chạy ngay trên máy cá nhân.

Việc kiểm thử cục bộ giúp:

- Giảm thời gian triển khai.
- Không tiêu tốn AWS Credits.
- Phát hiện lỗi sớm trước khi triển khai lên môi trường thực.

---

# Xây dựng Data Pipeline

Sau khi có hạ tầng, tiến hành xây dựng một **Data Pipeline** đơn giản.

Luồng dữ liệu bao gồm:

```
Event Source
      ↓
Kinesis Data Streams
      ↓
Amazon Data Firehose
      ↓
Amazon S3
      ↓
AWS Glue
      ↓
Amazon Athena
      ↓
Amazon Redshift
      ↓
Amazon QuickSight
```

Pipeline này mô phỏng toàn bộ vòng đời dữ liệu từ quá trình thu thập, lưu trữ, xử lý cho đến trực quan hóa.

---

# AWS Glue

Tiếp theo là tìm hiểu **AWS Glue**, dịch vụ ETL Serverless của AWS.

Các thành phần quan trọng gồm:

- Glue Data Catalog
- Glue Crawlers
- Glue ETL Jobs
- Glue Studio
- Glue DataBrew

Glue giúp tự động:

- Phát hiện Schema.
- Quản lý Metadata.
- Chuyển đổi dữ liệu.
- Chuẩn hóa dữ liệu trước khi phân tích.

Điều này giúp giảm đáng kể công việc xây dựng pipeline ETL thủ công.

---

# Amazon Athena

Sau khi dữ liệu được lưu trên Amazon S3 và được Glue Catalog quản lý, có thể sử dụng **Amazon Athena** để truy vấn trực tiếp.

Athena là dịch vụ SQL Serverless cho phép:

- Truy vấn dữ liệu trên Amazon S3.
- Không cần triển khai Database.
- Không cần quản lý Server.
- Chỉ trả phí theo lượng dữ liệu được quét.

Athena hỗ trợ nhiều định dạng dữ liệu như:

- CSV
- JSON
- Parquet
- ORC
- Avro

Việc sử dụng định dạng cột như **Parquet** giúp giảm đáng kể chi phí truy vấn.

---

# Thực hành triển khai Amazon RDS

Hoạt động thực hành cuối cùng trong ngày là triển khai cơ sở dữ liệu quan hệ bằng **Amazon RDS**.

Các bước thực hiện bao gồm:

- Tạo DB Subnet Group.
- Cấu hình Security Group.
- Khởi tạo PostgreSQL hoặc MySQL.
- Kết nối tới Database.
- Xóa tài nguyên sau khi hoàn thành.

Trong quá trình này cũng tìm hiểu cách:

- Triển khai Database trong VPC.
- Cấu hình Private Subnet.
- Quản lý Backup.
- Thiết lập quyền truy cập an toàn thông qua Security Group.

Amazon RDS giúp loại bỏ phần lớn công việc quản trị cơ sở dữ liệu như sao lưu, cập nhật và bảo trì hệ thống.

---

# Bài học rút ra

- Hiểu cách quản lý hạ tầng bằng Infrastructure as Code thông qua AWS CloudFormation và AWS CDK.
- Biết cách kiểm thử kiến trúc AWS cục bộ bằng Floci và LocalStack trước khi triển khai lên môi trường thực.
- Xây dựng được quy trình Data Pipeline từ thu thập dữ liệu đến phân tích.
- Hiểu vai trò của AWS Glue trong quy trình ETL và Amazon Athena trong việc truy vấn dữ liệu trên Data Lake.
- Thực hành triển khai Amazon RDS và nắm được các thành phần mạng liên quan như VPC, DB Subnet Group và Security Group.
- Nhận thấy việc tự động hóa hạ tầng và pipeline giúp quá trình phát triển nhanh hơn, dễ bảo trì hơn và giảm thiểu sai sót khi triển khai.

---

*Nguồn tài liệu chính: https://cloudjourney.awsstudygroup.com/*