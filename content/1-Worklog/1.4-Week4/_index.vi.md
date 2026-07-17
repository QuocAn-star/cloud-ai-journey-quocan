---
title: "Worklog Tuần 4"
date: 2026-05-10
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
---

**Thời gian:** 11/05/2026 - 15/05/2026

## Mục tiêu tuần 4

- Tìm hiểu bài toán Customer Behavior Analytics và yêu cầu của hệ thống.
- Nghiên cứu kiến trúc Data Lakehouse theo mô hình Medallion.
- Khảo sát bộ dữ liệu và xác định các nguồn dữ liệu phục vụ dự án.
- Thiết kế kiến trúc tổng thể của hệ thống trước khi triển khai.

### Các công việc cần triển khai trong tuần này

| Thứ | Công việc | Ngày | Nguồn tài liệu |
|:---:|-----------|:----:|----------------|
| **2** | Tìm hiểu bài toán Customer Behavior Analytics, nghiên cứu đặc điểm của dữ liệu hành vi khách hàng trong thương mại điện tử, xác định mục tiêu phân tích và các chỉ số cần xây dựng để phục vụ việc trực quan hóa dữ liệu. | 11/05/2026 | https://aws.amazon.com/big-data/datalakes-and-analytics/ |
| **3** | Nghiên cứu kiến trúc Data Lakehouse và mô hình Medallion Architecture, tìm hiểu vai trò của ba tầng Bronze, Silver và Gold trong việc lưu trữ, làm sạch và tổng hợp dữ liệu phục vụ phân tích. | 12/05/2026 | https://www.databricks.com/glossary/medallion-architecture |
| **4** | Thiết kế kiến trúc tổng thể của hệ thống trên AWS, xác định vai trò của Amazon S3, AWS Glue, AWS Glue Data Catalog, Amazon Athena, Amazon Kinesis Data Firehose, Amazon EC2 và Streamlit trong quy trình xử lý dữ liệu. | 13/05/2026 | https://aws.amazon.com/architecture/ |
| **5** | Khảo sát bộ dữ liệu Customer Behavior Analytics, phân tích cấu trúc dữ liệu đầu vào, xác định các trường dữ liệu cần xử lý và lập kế hoạch xây dựng quy trình Data Ingestion phục vụ Batch Processing và Streaming Processing. | 14/05/2026 | https://www.kaggle.com/datasets/wafaaelhusseini/e-commerce-transactions-clickstream |
| **6** | Hoàn thiện thiết kế kiến trúc hệ thống, xây dựng sơ đồ luồng xử lý dữ liệu từ Data Ingestion đến Dashboard và chuẩn bị môi trường để triển khai các thành phần của dự án trong các tuần tiếp theo. | 15/05/2026 | AWS Document |


## Kết quả đạt được

- Hiểu rõ yêu cầu của bài toán Customer Behavior Analytics.
- Hoàn thành việc khảo sát và phân tích bộ dữ liệu sử dụng trong dự án.
- Nắm được kiến trúc Medallion Data Lakehouse và vai trò của từng tầng dữ liệu.
- Hoàn thành thiết kế kiến trúc tổng thể và xác định được quy trình xử lý dữ liệu Batch và Streaming.
- Chuẩn bị đầy đủ nền tảng để bắt đầu triển khai hệ thống Data Lakehouse trong các tuần tiếp theo.