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

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Xây dựng cấu trúc lưu trữ dữ liệu trên Amazon S3 theo mô hình Data Lakehouse, tạo các thư mục phục vụ cho Raw Data, Bronze Layer và Streaming Data nhằm chuẩn bị môi trường lưu trữ cho toàn bộ hệ thống. | 18/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| **3** | Triển khai quy trình Batch Processing bằng cách thu thập dữ liệu khách hàng, đơn hàng và sản phẩm từ bộ dữ liệu, sau đó tải dữ liệu lên Amazon S3 để làm nguồn đầu vào cho quá trình xử lý dữ liệu. | 19/05/2026 | AWS Document |
| **4** | Nghiên cứu Amazon Kinesis Data Firehose và triển khai Streaming Processing để tiếp nhận dữ liệu sự kiện theo thời gian thực, đồng thời cấu hình Firehose ghi dữ liệu trực tiếp vào Amazon S3. | 20/05/2026 | https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html |
| **5** | Kiểm tra dữ liệu được lưu trữ trong Bronze Layer, xác nhận dữ liệu Batch và Streaming được ghi đầy đủ vào Amazon S3, đồng thời đánh giá tính toàn vẹn của dữ liệu trước khi thực hiện các bước chuyển đổi tiếp theo. | 21/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html |
| **6** | Hoàn thiện quy trình Data Ingestion, rà soát cấu trúc lưu trữ dữ liệu và chuẩn bị nguồn dữ liệu cho quá trình xử lý bằng AWS Glue ETL ở giai đoạn tiếp theo. | 22/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |


## Kết quả đạt được

- Hoàn thành việc xây dựng tầng lưu trữ Bronze trên Amazon S3.
- Tổ chức dữ liệu theo kiến trúc Medallion Data Lakehouse.
- Thực hiện thành công quá trình thu thập dữ liệu Batch và nghiên cứu cơ chế Streaming Data Ingestion.
- Xác định được luồng dữ liệu từ nguồn đến Bronze Layer.
- Chuẩn bị đầy đủ dữ liệu phục vụ cho quá trình xử lý bằng AWS Glue trong các tuần tiếp theo.