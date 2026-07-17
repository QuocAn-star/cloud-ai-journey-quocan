---
title: "Worklog Tuần 5"
date: 2026-05-18
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
---

**Thời gian:** 18/05/2026 - 22/05/2026

## Mục tiêu tuần 5

- Xây dựng tầng lưu trữ Bronze trong kiến trúc Data Lakehouse.
- Chuẩn bị môi trường lưu trữ dữ liệu trên Amazon S3.
- Thực hiện quá trình thu thập và lưu trữ dữ liệu từ nhiều nguồn vào hệ thống.
- Tìm hiểu quy trình Data Ingestion cho cả Batch Processing và Streaming Processing.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
|:---:|-----------|:------------:|:---------------:|----------------|
| **2** | - Tạo Amazon S3 Bucket cho dự án.<br>- Thiết kế cấu trúc thư mục theo mô hình Bronze, Silver và Gold. | 18/05/2026 | 18/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| **3** | - Chuẩn bị bộ dữ liệu Customer Behavior Analytics.<br>- Upload dữ liệu Batch lên Amazon S3.<br>- Kiểm tra cấu trúc dữ liệu sau khi tải lên. | 19/05/2026 | 19/05/2026 | https://www.kaggle.com/datasets/wafaaelhusseini/e-commerce-transactions-clickstream |
| **4** | - Nghiên cứu quy trình Streaming Data Ingestion.<br>- Tìm hiểu Amazon Kinesis Data Firehose và cơ chế truyền dữ liệu vào Amazon S3. | 20/05/2026 | 20/05/2026 | https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html?utm_source=chatgpt.com |
| **5** | - Thiết kế luồng Data Ingestion cho Batch và Streaming.<br>- Kiểm tra dữ liệu tại tầng Bronze sau khi tiếp nhận. | 21/05/2026 | 21/05/2026 | https://docs.aws.amazon.com/msk/latest/developerguide/integrations-redshift.html |
| **6** | - Đánh giá kết quả thu thập dữ liệu.<br>- Chuẩn hóa cấu trúc lưu trữ dữ liệu trong Bronze Layer.<br>- Chuẩn bị dữ liệu cho giai đoạn xử lý bằng AWS Glue. | 22/05/2026 | 22/05/2026 | AWS Prescriptive Guidance |

## Kết quả đạt được

- Hoàn thành việc xây dựng tầng lưu trữ Bronze trên Amazon S3.
- Tổ chức dữ liệu theo kiến trúc Medallion Data Lakehouse.
- Thực hiện thành công quá trình thu thập dữ liệu Batch và nghiên cứu cơ chế Streaming Data Ingestion.
- Xác định được luồng dữ liệu từ nguồn đến Bronze Layer.
- Chuẩn bị đầy đủ dữ liệu phục vụ cho quá trình xử lý bằng AWS Glue trong các tuần tiếp theo.