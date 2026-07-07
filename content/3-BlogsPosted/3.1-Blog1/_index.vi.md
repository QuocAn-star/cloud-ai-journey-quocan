---
title: "Blog 1"
date: 2026-01-01
weight: 1
chapter: false
pre: " <b> 3.1. </b> "
---

# Xây dựng Pipeline CDC Thời Gian Thực: Từ Amazon Aurora sang Amazon S3 Tables với Debezium và Firehose

> **Bài gốc:** [Real-time CDC from Aurora PostgreSQL to Amazon S3 Tables using Debezium and Firehose](https://aws.amazon.com/blogs/big-data/real-time-cdc-from-aurora-postgresql-to-amazon-s3-tables-using-debezium-and-firehose/)

> **Bài dịch:** [Real-time CDC from Aurora PostgreSQL to Amazon S3 Tables using Debezium and Firehose](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2199216520843308/?rdid=AAZBwZqs23GM5W9s#)

---

Trong kỷ nguyên dữ liệu hiện nay, việc tách biệt dữ liệu giao dịch (OLTP) và dữ liệu phân tích (OLAP) là cực kỳ quan trọng. Nếu bạn chạy các truy vấn phân tích nặng nề trực tiếp trên cụm Amazon Aurora, hiệu năng hệ thống giao dịch chắc chắn sẽ bị ảnh hưởng.

Thông thường, chúng ta dùng phương pháp xuất dữ liệu theo lô (batch), nhưng cách này lại tạo ra độ trễ lớn. Bài viết này sẽ giới thiệu cho bạn một giải pháp mạnh mẽ hơn: **Real-time Change Data Capture (CDC)** để đưa dữ liệu từ Aurora PostgreSQL sang **Amazon S3 Tables** dưới định dạng Apache Iceberg, giúp dữ liệu luôn sẵn sàng để truy vấn ngay lập tức.

---

## 1. Tại sao lại là Amazon S3 Tables và Apache Iceberg?

Khác với các phương pháp CDC truyền thống chỉ ghi lại nhật ký thay đổi (append-only), định dạng **Apache Iceberg** cho phép thực hiện các thao tác **cập nhật (update)** và **xóa (delete)** ở cấp độ dòng dữ liệu.

Đặc biệt, **Amazon S3 Tables** còn tự động hóa các công việc bảo trì phức tạp như quản lý snapshot hay nén dữ liệu (compaction), giúp các kỹ sư dữ liệu rảnh tay hơn. Bạn còn có thể sử dụng tính năng **Time Travel** của Iceberg để truy vấn dữ liệu tại một thời điểm trong quá khứ.

---

## 2. Kiến trúc của hệ thống: 6 thành phần cốt lõi

Hệ thống được thiết kế tối ưu với 6 bước truyền dẫn dữ liệu:

| Bước | Từ → Đến | Mô tả |
|------|----------|-------|
| 1 | Aurora PostgreSQL → Debezium | Debezium chạy trên MSK Connect đọc thay đổi từ WAL của PostgreSQL, hầu như không gây áp lực hiệu năng |
| 2 | Debezium → Amazon MSK | `ByLogicalTableRouter` gộp thay đổi từ nhiều bảng vào một Kafka topic - tiết kiệm chi phí và giảm độ phức tạp |
| 3 | Amazon MSK → Firehose | Amazon Data Firehose liên tục thăm dò dữ liệu từ MSK qua AWS PrivateLink |
| 4 | AWS Lambda | "Bộ não" chuyển đổi - giải mã dữ liệu, làm phẳng cấu trúc Debezium, gắn metadata (tên bảng + loại thao tác) |
| 5 | Firehose → S3 Tables | Firehose dựa vào metadata từ Lambda để đẩy vào đúng bảng Iceberg tương ứng |
| 6 | Truy vấn & Phân quyền | Dữ liệu sẵn sàng truy vấn qua Amazon Athena hoặc Redshift, kiểm soát bởi AWS Lake Formation |

---

## 3. Cơ chế chuyển đổi dữ liệu thông minh

Điểm thú vị nhất của giải pháp nằm ở cách Lambda ánh xạ mã thao tác từ Debezium sang Firehose:

| Mã Debezium | Ý nghĩa | Thao tác Firehose |
|---|---|---|
| `c` (Create) / `r` (Read) | Tạo mới | → **Insert** vào bảng Iceberg |
| `u` (Update) | Cập nhật | → **Upsert** dựa trên khóa chính |
| `d` (Delete) | Xóa | → **Delete** dòng tương ứng |

Nhờ cơ chế này, bảng đích tại S3 Tables luôn là một **bản sao hoàn hảo** về trạng thái hiện tại của cơ sở dữ liệu nguồn.

---

## 4. Triển khai nhanh chóng với AWS CDK

Thay vì phải cấu hình thủ công từng dịch vụ, bạn có thể triển khai toàn bộ hạ tầng này thông qua mã nguồn với **AWS CDK**. Quy trình bao gồm:

1. Bật tính năng `logical_replication` trên Aurora.
2. Đóng gói và đăng ký Debezium plugin trên MSK Connect.
3. Sử dụng lệnh `cdk deploy` để khởi tạo toàn bộ **6 stack tài nguyên** từ MSK cluster cho đến S3 Tables bucket.

Giải pháp này không chỉ giúp bạn xây dựng một **Data Lakehouse** gần như thời gian thực mà còn cực kỳ tối ưu về chi phí nhờ việc gộp nhiều bảng vào một luồng dữ liệu duy nhất.

---

## Bài học rút ra

- **CDC + Iceberg = Phân tích thời gian thực mà không gây áp lực lên Aurora**
- Gộp nhiều bảng vào một Kafka topic giúp tiết kiệm chi phí đáng kể
- Lambda là cầu nối giữa định dạng Debezium và yêu cầu của Firehose
- AWS CDK giúp toàn bộ hạ tầng có thể tái tạo và quản lý phiên bản

---

*Hình ảnh minh họa:*

![Blog 1 - Pipeline CDC Thời Gian Thực](/images/blog1.jpg)
