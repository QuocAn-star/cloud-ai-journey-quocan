---
title: "Bản đề xuất"
date: 2026-05-16
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# 1. Tổng quan dự án

Dự án đề xuất xây dựng **FinOps-Optimized Serverless Medallion Data Lakehouse Architecture for Customer Behavior Analytics trên nền tảng AWS**.

Mục tiêu của dự án là xây dựng một nền tảng dữ liệu hoàn chỉnh có khả năng thu thập, lưu trữ, xử lý, truy vấn và trực quan hóa dữ liệu hành vi khách hàng bằng các dịch vụ Serverless của AWS. Hệ thống được thiết kế theo kiến trúc **Medallion Data Lakehouse**, tổ chức dữ liệu thành bốn tầng gồm **Raw, Bronze, Silver và Gold** nhằm nâng cao chất lượng dữ liệu, tối ưu hiệu năng truy vấn và hỗ trợ quá trình phân tích.

Dự án mô phỏng quy trình xử lý dữ liệu trong thực tế bằng cách kết hợp **Batch Processing** và **Streaming Processing**, sử dụng các dịch vụ như Amazon S3, AWS Glue, AWS Glue Data Catalog, Amazon Athena, AWS Lambda, Amazon Kinesis Data Firehose, Amazon EventBridge và Amazon EC2.

Bên cạnh việc xây dựng pipeline xử lý dữ liệu, dự án còn phát triển Dashboard bằng Streamlit giúp trực quan hóa các chỉ số kinh doanh và hành vi khách hàng thông qua các biểu đồ phân tích.

---

# 2. Bối cảnh và vấn đề cần giải quyết

Trong quá trình hoạt động, doanh nghiệp tạo ra lượng lớn dữ liệu từ nhiều nguồn khác nhau như đơn hàng, khách hàng, sản phẩm, phương thức thanh toán và các sự kiện tương tác của người dùng. Nếu dữ liệu chỉ được lưu trữ rời rạc hoặc xử lý thủ công sẽ rất khó quản lý, phân tích và khai thác hiệu quả.

Các hệ thống Data Warehouse truyền thống phù hợp cho báo cáo nhưng còn hạn chế về khả năng mở rộng và xử lý nhiều nguồn dữ liệu khác nhau. Trong khi đó, Data Lake có khả năng lưu trữ dữ liệu lớn nhưng thiếu cơ chế quản lý dữ liệu và tối ưu cho phân tích.

Kiến trúc **Data Lakehouse** kết hợp ưu điểm của cả Data Lake và Data Warehouse, giúp doanh nghiệp vừa lưu trữ dữ liệu với chi phí thấp, vừa xử lý và phân tích dữ liệu hiệu quả.

Dự án này xây dựng một hệ thống Customer Behavior Analytics trên AWS nhằm mô phỏng toàn bộ quy trình từ thu thập dữ liệu, xử lý ETL, quản lý dữ liệu theo mô hình Medallion đến truy vấn và trực quan hóa kết quả phục vụ phân tích kinh doanh.

Ngoài ra, dự án cũng áp dụng tư tưởng **FinOps**, ưu tiên sử dụng các dịch vụ Serverless nhằm giảm chi phí vận hành và hạn chế việc quản lý hạ tầng.

---

# 3. Mục tiêu dự án

## 3.1. Mục tiêu tổng quát

Xây dựng hệ thống **Customer Behavior Analytics** theo kiến trúc **FinOps-Optimized Serverless Medallion Data Lakehouse** trên AWS, hỗ trợ toàn bộ quy trình từ thu thập dữ liệu, xử lý ETL, lưu trữ, phân tích đến trực quan hóa dữ liệu.

## 3.2. Mục tiêu cụ thể

- Xây dựng hai pipeline thu thập dữ liệu gồm **Batch Processing** và **Streaming Processing**.
- Lưu trữ dữ liệu trên Amazon S3 theo mô hình **Raw, Bronze, Silver và Gold**.
- Xây dựng AWS Glue ETL Jobs để xử lý dữ liệu giữa các tầng.
- Thực hiện làm sạch, chuẩn hóa và tổng hợp dữ liệu.
- Quản lý metadata bằng AWS Glue Data Catalog.
- Truy vấn dữ liệu bằng Amazon Athena.
- Phát triển Dashboard phân tích bằng Streamlit.
- Triển khai Dashboard trên Amazon EC2.
- Áp dụng các nguyên tắc FinOps nhằm tối ưu chi phí sử dụng dịch vụ AWS.
- Xây dựng một hệ thống Data Lakehouse hoàn chỉnh phục vụ bài toán Customer Behavior Analytics.

---

# 4. Phạm vi dự án

## 4.1. Trong phạm vi

Dự án tập trung triển khai các nội dung sau:

- Thiết kế kiến trúc Data Lakehouse trên AWS.
- Xây dựng Batch Processing và Streaming Processing.
- Triển khai các tầng Raw, Bronze, Silver và Gold trên Amazon S3.
- Phát triển AWS Glue ETL Jobs để xử lý dữ liệu.
- Quản lý metadata bằng AWS Glue Data Catalog.
- Truy vấn dữ liệu bằng Amazon Athena.
- Xây dựng Dashboard bằng Streamlit.
- Triển khai Dashboard trên Amazon EC2.
- Hoàn thiện tài liệu hướng dẫn triển khai và báo cáo dự án.

## 4.2. Ngoài phạm vi

Dự án không bao gồm các nội dung sau:

- Xây dựng hệ thống Machine Learning hoặc AI Recommendation.
- Triển khai hệ thống ở quy mô doanh nghiệp hoặc nhiều khu vực (Multi-Region).
- Thiết kế hệ thống bảo mật chuyên sâu.
- Xây dựng ứng dụng Web hoặc Mobile dành cho khách hàng.
- Triển khai hệ thống CI/CD và giám sát ở mức Production.
- Xử lý dữ liệu có quy mô Big Data bằng Apache Spark Cluster.

# 5. Kiến trúc giải pháp

Kiến trúc của hệ thống được xây dựng theo mô hình **FinOps-Optimized Serverless Medallion Data Lakehouse** trên nền tảng AWS.

Hệ thống được chia thành năm thành phần chính:

- **Data Ingestion Layer:** Thu thập dữ liệu từ Batch Processing và Streaming Processing.
- **Storage Layer:** Lưu trữ dữ liệu trên Amazon S3 theo mô hình Medallion.
- **Processing Layer:** Thực hiện ETL và chuyển đổi dữ liệu bằng AWS Glue.
- **Query Layer:** Quản lý metadata và truy vấn dữ liệu bằng AWS Glue Data Catalog và Amazon Athena.
- **Visualization Layer:** Hiển thị dữ liệu thông qua Dashboard được xây dựng bằng Streamlit và triển khai trên Amazon EC2.

Sơ đồ kiến trúc tổng thể như sau:

![Customer Behavior Analytics Architecture](/images/2-Proposal/customer_behavior_architecture.png)

## 5.1. Data Ingestion Layer

Luồng Batch Processing:

```text
Database
    │
    ▼
AWS Lambda
    │
    ▼
Amazon S3 (Raw Layer)
```

Luồng Streaming Processing:

```text
Application / Event Source
        │
        ▼
Amazon Kinesis Data Firehose
        │
        ▼
Amazon S3 (Raw Layer)
```

Các bước chính:

1. Dữ liệu Batch được đồng bộ theo lịch bằng Amazon EventBridge và AWS Lambda.
2. Dữ liệu Streaming được tiếp nhận liên tục thông qua Amazon Kinesis Data Firehose.
3. Toàn bộ dữ liệu được lưu vào Raw Layer trên Amazon S3 để phục vụ quá trình xử lý.

---

## 5.2. Data Processing Layer

Luồng xử lý dữ liệu:

```text
Raw Layer
     │
     ▼
Bronze Layer
     │
     ▼
Silver Layer
     │
     ▼
Gold Layer
```

Các bước chính:

1. AWS Glue ETL đọc dữ liệu từ Raw Layer và chuyển sang Bronze Layer.
2. Bronze Layer lưu dữ liệu gần với dữ liệu gốc sau khi chuẩn hóa định dạng.
3. Silver Layer thực hiện làm sạch dữ liệu, loại bỏ dữ liệu trùng lặp và chuẩn hóa kiểu dữ liệu.
4. Gold Layer tổng hợp dữ liệu để phục vụ phân tích và báo cáo.

---

## 5.3. Query & Visualization Layer

Luồng phân tích dữ liệu:

```text
Gold Layer
      │
      ▼
AWS Glue Data Catalog
      │
      ▼
Amazon Athena
      │
      ▼
Streamlit Dashboard
      │
      ▼
Amazon EC2
```

Các bước chính:

1. Các bảng trong Gold Layer được đăng ký vào AWS Glue Data Catalog.
2. Amazon Athena thực hiện truy vấn SQL trực tiếp trên dữ liệu lưu trữ trong Amazon S3.
3. Dashboard sử dụng AWS Wrangler để đọc dữ liệu từ Amazon Athena.
4. Streamlit trực quan hóa các chỉ số phân tích và được triển khai trên Amazon EC2 để người dùng truy cập.

---

# 6. Dịch vụ AWS sử dụng và lý do lựa chọn

| Dịch vụ | Vai trò trong hệ thống | Lý do lựa chọn |
| --- | --- | --- |
| Amazon S3 | Lưu trữ dữ liệu Raw, Bronze, Silver và Gold | Chi phí thấp, khả năng mở rộng cao và phù hợp làm Data Lake |
| AWS Glue | Thực hiện ETL giữa các tầng dữ liệu | Serverless, dễ tích hợp với Amazon S3 |
| AWS Glue Data Catalog | Quản lý metadata của các bảng dữ liệu | Hỗ trợ Amazon Athena và Glue ETL |
| Amazon Athena | Truy vấn dữ liệu bằng SQL | Không cần quản lý máy chủ, truy vấn trực tiếp trên Amazon S3 |
| AWS Lambda | Xử lý dữ liệu Batch | Tự động thực thi theo sự kiện hoặc lịch |
| Amazon Kinesis Data Firehose | Thu thập dữ liệu Streaming | Hỗ trợ ghi dữ liệu liên tục vào Amazon S3 |
| Amazon EventBridge | Lập lịch Batch Processing | Tự động hóa quá trình đồng bộ dữ liệu |
| Amazon EC2 | Triển khai Dashboard | Cung cấp môi trường chạy ứng dụng Streamlit |
| IAM | Quản lý quyền truy cập | Đảm bảo an toàn giữa các dịch vụ AWS |

---

# 7. Dữ liệu sử dụng

## 7.1. Dữ liệu đầu vào

Dự án sử dụng bộ dữ liệu Customer Behavior bao gồm các thông tin như:

- Customer Information.
- Orders.
- Products.
- User Events.
- Traffic Sources.
- Payment Methods.
- Countries.
- Devices.

Các dữ liệu được thu thập thông qua hai pipeline gồm Batch Processing và Streaming Processing trước khi đưa vào hệ thống Data Lakehouse.

---

## 7.2. Quá trình xử lý dữ liệu

Dữ liệu được xử lý theo kiến trúc Medallion gồm bốn tầng:

- **Raw Layer:** Lưu trữ dữ liệu gốc.
- **Bronze Layer:** Chuẩn hóa định dạng dữ liệu.
- **Silver Layer:** Làm sạch và chuẩn hóa dữ liệu.
- **Gold Layer:** Tổng hợp dữ liệu phục vụ phân tích và trực quan hóa.

Sau khi hoàn thành quá trình ETL, các bảng Gold sẽ được đăng ký vào AWS Glue Data Catalog để phục vụ truy vấn bằng Amazon Athena và hiển thị trên Dashboard.

---

## 7.3. Kết quả đầu ra

Hệ thống tạo ra các bảng dữ liệu phân tích phục vụ Dashboard như:

- Dashboard Summary.
- Daily Revenue.
- Event Summary.
- Country Revenue.
- Device Summary.
- Payment Summary.
- Source Summary.

Các bảng này cung cấp các chỉ số KPI và dữ liệu tổng hợp phục vụ phân tích hành vi khách hàng và hỗ trợ ra quyết định.

# 8. Lộ trình triển khai

| Giai đoạn | Thời gian dự kiến | Nội dung chính |
| --- | --- | --- |
| Giai đoạn 1 | Tuần 1 - Tuần 2 | Nghiên cứu AWS, Data Lakehouse và thiết kế kiến trúc hệ thống |
| Giai đoạn 2 | Tuần 3 - Tuần 4 | Xây dựng Data Ingestion Layer và triển khai Raw, Bronze Layer |
| Giai đoạn 3 | Tuần 5 - Tuần 6 | Xây dựng Silver Layer, Gold Layer và các AWS Glue ETL Jobs |
| Giai đoạn 4 | Tuần 7 - Tuần 8 | Thiết lập AWS Glue Data Catalog, Amazon Athena và phát triển Dashboard |
| Giai đoạn 5 | Tuần 9 - Tuần 10 | Triển khai Dashboard trên Amazon EC2 và tích hợp toàn bộ hệ thống |
| Giai đoạn 6 | Tuần 11 - Tuần 12 | Kiểm thử, tối ưu hệ thống, hoàn thiện tài liệu và chuẩn bị báo cáo |

---

# 9. Ước tính chi phí

Dự án được xây dựng theo mô hình **Serverless** nhằm giảm chi phí triển khai và vận hành. Các dịch vụ AWS chỉ phát sinh chi phí khi sử dụng, phù hợp với quy mô của dự án thực tập.

Các dịch vụ chính phát sinh chi phí bao gồm:

- Amazon S3.
- AWS Glue.
- Amazon Athena.
- Amazon EC2.
- AWS Lambda.
- Amazon Kinesis Data Firehose.

Để tối ưu chi phí, các tài nguyên không sử dụng sẽ được dừng hoặc xóa sau khi hoàn thành quá trình kiểm thử và trình diễn hệ thống.

---

# 10. Rủi ro và phương án giảm thiểu

| Rủi ro | Ảnh hưởng | Phương án giảm thiểu |
| --- | --- | --- |
| ETL Job xử lý thất bại | Cao | Kiểm tra AWS Glue Logs và chuẩn hóa dữ liệu đầu vào |
| Lỗi truy vấn Amazon Athena | Trung bình | Kiểm tra Glue Data Catalog và cấu trúc bảng |
| Chi phí AWS tăng ngoài dự kiến | Trung bình | Áp dụng FinOps, xóa tài nguyên không sử dụng sau khi hoàn thành |
| Dashboard không kết nối được với Athena | Trung bình | Kiểm tra IAM Role, AWS Credentials và cấu hình Region |
| Lỗi khi triển khai Dashboard trên EC2 | Thấp | Kiểm tra Security Group, Network và cấu hình Streamlit |

---

# 11. Kết quả kỳ vọng

Sau khi hoàn thành, dự án kỳ vọng đạt được các kết quả sau:

- Xây dựng thành công kiến trúc Data Lakehouse trên AWS.
- Triển khai đầy đủ Batch Processing và Streaming Processing.
- Hoàn thành các tầng Raw, Bronze, Silver và Gold.
- Xây dựng các AWS Glue ETL Jobs phục vụ xử lý dữ liệu.
- Truy vấn dữ liệu thành công bằng Amazon Athena.
- Hoàn thành Dashboard trực quan hóa dữ liệu bằng Streamlit.
- Triển khai Dashboard trên Amazon EC2.
- Hoàn thiện tài liệu triển khai và báo cáo dự án.

---

# 12. Hướng phát triển trong tương lai

Trong tương lai, hệ thống có thể được mở rộng theo các hướng sau:

- Tích hợp Apache Spark để xử lý dữ liệu có quy mô lớn.
- Xây dựng Dashboard với nhiều KPI và biểu đồ phân tích hơn.
- Áp dụng CI/CD để tự động triển khai Dashboard.
- Tích hợp Machine Learning nhằm dự đoán hành vi khách hàng.
- Tối ưu hiệu năng và chi phí vận hành theo các nguyên tắc FinOps.
- Mở rộng hệ thống để xử lý dữ liệu theo thời gian thực với quy mô lớn hơn.