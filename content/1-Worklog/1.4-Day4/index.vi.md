---
title: "Ngày 4"
date: 2026-04-23
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
---

> **Ngày 4 - Phân tích Dữ liệu Lớn trên AWS:** Tìm hiểu Amazon EMR, Amazon Kinesis, Amazon Data Firehose, AWS Lake Formation, Amazon Redshift và Amazon QuickSight để hiểu cách các dịch vụ AWS phối hợp xây dựng một nền tảng phân tích dữ liệu hiện đại.

---

## Mục tiêu trong ngày

- Hiểu kiến trúc của một nền tảng phân tích dữ liệu hiện đại trên AWS.
- Tìm hiểu cách thu thập dữ liệu thời gian thực bằng Amazon Kinesis.
- Khám phá Amazon Data Firehose để tự động phân phối dữ liệu.
- Hiểu vai trò của Amazon EMR trong xử lý dữ liệu quy mô lớn.
- Tìm hiểu cách quản trị dữ liệu tập trung với AWS Lake Formation.
- So sánh Amazon Redshift và Amazon Athena cho các nhu cầu phân tích dữ liệu.
- Trực quan hóa dữ liệu bằng Amazon QuickSight.

---

# Kiến trúc Phân tích Dữ liệu Hiện đại

Nội dung cuối cùng tập trung vào việc tìm hiểu cách nhiều dịch vụ AWS kết hợp với nhau để xây dựng một nền tảng phân tích dữ liệu hoàn chỉnh.

Một quy trình xử lý dữ liệu điển hình bao gồm:

```
Nguồn dữ liệu
      ↓
Amazon Kinesis Data Streams
      ↓
Amazon Data Firehose
      ↓
Amazon S3
      ↓
AWS Glue Data Catalog
      ↓
Amazon Athena
      ↓
Amazon Redshift
      ↓
Amazon QuickSight
```

Kiến trúc này mô tả toàn bộ vòng đời của dữ liệu, từ quá trình thu thập, lưu trữ, xử lý, phân tích cho đến trực quan hóa.

---

# Amazon EMR

Dịch vụ đầu tiên được tìm hiểu là **Amazon EMR (Elastic MapReduce)**, nền tảng xử lý dữ liệu lớn được AWS quản lý.

Amazon EMR hỗ trợ nhiều framework mã nguồn mở phổ biến như:

- Apache Spark
- Apache Hadoop
- Apache Hive
- Apache Presto
- Apache Flink

EMR được thiết kế để xử lý các tập dữ liệu có quy mô từ terabyte đến petabyte, đồng thời tự động quản lý hạ tầng và mở rộng tài nguyên khi cần thiết.

Các mô hình triển khai được tìm hiểu gồm:

- EMR on EC2
- EMR Serverless
- EMR on EKS

Trong đó, **EMR Serverless** giúp đơn giản hóa việc vận hành bằng cách tự động cấp phát tài nguyên và tự động thu hồi khi không còn tác vụ xử lý.

---

# Amazon Kinesis

Tiếp theo là **Amazon Kinesis**, nền tảng xử lý dữ liệu thời gian thực của AWS.

## Amazon Kinesis Data Streams

Amazon Kinesis Data Streams cho phép thu thập liên tục dữ liệu streaming từ nhiều nguồn khác nhau.

Các khái niệm quan trọng bao gồm:

- Shards
- Partition Keys
- Sequence Numbers
- Retention Period
- Consumers

Một số trường hợp sử dụng phổ biến:

- Thu thập log hệ thống
- Phân tích Clickstream
- Dữ liệu IoT
- Giao dịch tài chính
- Giám sát thời gian thực

Kinesis cung cấp khả năng xử lý dữ liệu với thông lượng cao và độ trễ thấp.

---

# Amazon Data Firehose

Sau khi dữ liệu được thu thập qua Kinesis Data Streams, **Amazon Data Firehose** chịu trách nhiệm tự động chuyển dữ liệu đến các hệ thống lưu trữ hoặc phân tích.

Firehose hỗ trợ nhiều đích lưu trữ như:

- Amazon S3
- Amazon Redshift
- Amazon OpenSearch
- Splunk
- HTTP Endpoint

Các tính năng nổi bật gồm:

- Buffering tự động
- Nén dữ liệu
- Chuyển đổi định dạng
- Chuyển đổi dữ liệu bằng AWS Lambda
- Tự động mở rộng

Khác với Kinesis Data Streams, Firehose không yêu cầu quản lý Shards, giúp đơn giản hóa việc xây dựng các pipeline streaming.

---

# AWS Lake Formation

Tiếp theo là **AWS Lake Formation**, dịch vụ quản trị Data Lake tập trung của AWS.

Lake Formation giúp đơn giản hóa việc xây dựng và quản lý Data Lake thông qua cơ chế phân quyền thống nhất.

Các khả năng chính gồm:

- Quản lý quyền truy cập tập trung
- Bảo mật theo cột (Column-level Security)
- Bảo mật theo hàng (Row-level Security)
- Tích hợp với AWS Glue Data Catalog
- Chia sẻ dữ liệu giữa nhiều AWS Accounts
- Governed Tables

Thay vì quản lý riêng lẻ IAM Policies và S3 Bucket Policies, toàn bộ quyền truy cập có thể được quản lý tập trung trong Lake Formation.

Điều này giúp giảm đáng kể độ phức tạp trong các hệ thống dữ liệu doanh nghiệp.

---

# Amazon Redshift

Tiếp theo là **Amazon Redshift**, dịch vụ Data Warehouse của AWS.

Amazon Redshift được tối ưu cho các bài toán phân tích dữ liệu quy mô lớn (OLAP).

Các khái niệm được tìm hiểu gồm:

- Columnar Storage
- Massively Parallel Processing (MPP)
- Leader Node
- Compute Nodes
- Redshift Spectrum
- RA3 Nodes

Ngoài ra còn tìm hiểu **Amazon Redshift Serverless**, giúp tự động cấp phát và mở rộng tài nguyên theo khối lượng công việc.

---

## So sánh Amazon Redshift và Amazon Athena

Việc so sánh hai dịch vụ giúp hiểu rõ trường hợp sử dụng phù hợp của từng nền tảng.

| Amazon Athena | Amazon Redshift |
|---------------|-----------------|
| Truy vấn trực tiếp dữ liệu trên Amazon S3 | Lưu trữ dữ liệu trong Data Warehouse |
| Phù hợp cho truy vấn ngẫu nhiên (Ad-hoc) | Phù hợp cho các truy vấn phân tích lặp lại |
| Tính phí theo lượng dữ liệu quét | Tính phí theo tài nguyên tính toán |
| Không cần quản lý hạ tầng | Hiệu năng cao cho phân tích dữ liệu |

Việc lựa chọn giữa Athena và Redshift phụ thuộc vào đặc điểm của từng bài toán thay vì dịch vụ nào tốt hơn.

---

# Amazon QuickSight

Dịch vụ cuối cùng được tìm hiểu là **Amazon QuickSight**, nền tảng Business Intelligence (BI) của AWS.

QuickSight có thể kết nối trực tiếp tới nhiều nguồn dữ liệu như:

- Amazon Athena
- Amazon Redshift
- Amazon RDS
- Amazon S3
- Amazon Aurora

Các tính năng nổi bật gồm:

- Dashboard tương tác
- SPICE In-Memory Engine
- Embedded Analytics
- ML Insights
- Truy vấn bằng ngôn ngữ tự nhiên với Amazon Q

QuickSight giúp chuyển đổi dữ liệu phân tích thành các dashboard và báo cáo trực quan mà không cần triển khai hệ thống BI riêng.

---

# Quy trình Phân tích Dữ liệu Hoàn chỉnh

Sau khi tìm hiểu từng dịch vụ riêng lẻ, toàn bộ quy trình phân tích dữ liệu được tổng hợp lại.

| Lớp | Dịch vụ AWS | Vai trò |
|------|-------------|----------|
| Thu thập dữ liệu | Amazon Kinesis Data Streams | Thu thập dữ liệu thời gian thực |
| Phân phối dữ liệu | Amazon Data Firehose | Chuyển dữ liệu đến nơi lưu trữ |
| Lưu trữ | Amazon S3 | Data Lake |
| Metadata | AWS Glue Data Catalog | Quản lý Schema và Metadata |
| Quản trị | AWS Lake Formation | Quản lý quyền truy cập |
| Xử lý | Amazon EMR | Xử lý dữ liệu quy mô lớn |
| Phân tích | Amazon Athena / Amazon Redshift | Truy vấn và phân tích dữ liệu |
| Trực quan hóa | Amazon QuickSight | Dashboard và báo cáo |

Đây là một trong những kiến trúc phổ biến nhất để xây dựng nền tảng phân tích dữ liệu trên AWS.

---

# Bài học rút ra

- Hiểu cách các dịch vụ AWS phối hợp để xây dựng một nền tảng phân tích dữ liệu hoàn chỉnh.
- Nắm được quy trình thu thập dữ liệu thời gian thực với Amazon Kinesis và Amazon Data Firehose.
- Hiểu vai trò của Amazon EMR trong xử lý dữ liệu phân tán quy mô lớn.
- Biết cách AWS Lake Formation quản lý bảo mật và phân quyền tập trung cho Data Lake.
- Phân biệt được trường hợp sử dụng của Amazon Athena và Amazon Redshift.
- Hiểu cách Amazon QuickSight chuyển dữ liệu phân tích thành các dashboard trực quan.
- Có cái nhìn tổng quan về toàn bộ hệ sinh thái phân tích dữ liệu của AWS, từ thu thập dữ liệu đến Business Intelligence.

---

*Nguồn tài liệu chính: https://cloudjourney.awsstudygroup.com/*