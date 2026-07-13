---
title: "Tổng quan"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 5.1 </b> "
---

# Tổng quan Workshop

## Workshop này nói về điều gì?

Workshop này hướng dẫn bạn xây dựng một **FinOps-Optimized Serverless Medallion Data Lakehouse** trên AWS - một nền tảng phân tích dữ liệu cấp production được thiết kế để phân tích hành vi khách hàng trong lĩnh vực thương mại điện tử.

Ý tưởng cốt lõi là chứng minh cách các doanh nghiệp thương mại điện tử hiện đại có thể thu được **insights phân tích sâu** (xu hướng doanh thu, phân khúc khách hàng, phân tích thanh toán, hiệu suất kênh traffic) từ hai nguồn dữ liệu:

1. **Sự kiện clickstream real-time** từ ứng dụng web và mobile (đường streaming qua API Gateway → Firehose → S3)
2. **Bản ghi đơn hàng giao dịch** từ cơ sở dữ liệu thương mại điện tử (đường batch qua EventBridge → Lambda → S3)

...tất cả trong khi giữ hạ tầng **100% serverless** và hóa đơn hàng ngày dưới **$3/ngày** sử dụng thực tế.

---

## Bối cảnh Kinh doanh

Hãy tưởng tượng bạn là kỹ sư dữ liệu tại một công ty thương mại điện tử đang phát triển. Các bên liên quan kinh doanh của bạn hỏi:

- *"Những quốc gia nào tạo ra doanh thu nhiều nhất?"*
- *"Khách hàng của chúng ta ưa chuộng phương thức thanh toán nào?"*
- *"Loại thiết bị nào tạo ra nhiều đơn hàng nhất - mobile, desktop hay tablet?"*
- *"Xu hướng doanh thu hàng ngày trong năm qua như thế nào?"*
- *"Những sự kiện người dùng nào xảy ra thường xuyên nhất trên nền tảng của chúng ta?"*

Nếu không có nền tảng dữ liệu phù hợp, việc trả lời những câu hỏi này yêu cầu xuất CSV thủ công, chạy SQL ad-hoc trực tiếp trên cơ sở dữ liệu production, hoặc xây dựng các cụm kho dữ liệu luôn hoạt động tốn kém.

Workshop này xây dựng nền tảng trả lời tất cả những câu hỏi đó - tự động, đáng tin cậy và tiết kiệm chi phí - sử dụng các dịch vụ managed của AWS.

---

## Kết quả học tập

Sau khi hoàn thành workshop này, bạn sẽ có thể:

| Kỹ năng | Những gì bạn sẽ học |
|---------|---------------------|
| **VPC & Networking** | Tạo VPC, Subnet, Internet Gateway, Route Table, Security Group cho nền tảng dữ liệu bảo mật |
| **S3 Data Lake** | Thiết kế cấu trúc S3 nhiều tầng (Raw → Bronze → Silver → Gold) với bucket policy phù hợp |
| **AWS Glue ETL** | Viết các ETL job PySpark chuyển đổi dữ liệu qua các tầng Medallion |
| **Glue Data Catalog** | Đăng ký schema bảng theo chương trình - không cần crawler thủ công |
| **Amazon Athena** | Chạy các truy vấn SQL serverless trên dữ liệu S3 sử dụng Glue Data Catalog |
| **Streamlit trên EC2** | Triển khai dashboard web Python trên EC2 trong VPC |
| **CloudWatch Monitoring** | Thiết lập alarm và dashboard để quan sát pipeline |
| **IAM Security** | Áp dụng quyền hạn tối thiểu cho từng dịch vụ |
| **FinOps** | Hiểu cách định dạng Parquet giúp giảm chi phí truy vấn Athena |

---

## Tóm tắt Kiến trúc

Nền tảng được xây dựng trên **6 lớp chức năng**:

```
┌─────────────────────────────────────────────────────────┐
│  NGUỒN DỮ LIỆU                                         │
│  • Website/Mobile → sự kiện JSON real-time              │
│  • DB thương mại điện tử → xuất CSV batch định kỳ       │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  TẦNG TIẾP NHẬN                                        │
│  • API Gateway → Firehose → Lambda → S3 (streaming)    │
│  • EventBridge → Lambda (trích xuất DB) → S3 (batch)   │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  TẦNG LƯU TRỮ - KIẾN TRÚC MEDALLION                   │
│  S3: Raw → Bronze (Parquet) → Silver (sạch) → Gold     │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  TẦNG XỬ LÝ                                            │
│  • Glue ETL Job 1: Raw → Bronze (CSV sang Parquet)     │
│  • Glue ETL Job 2: Bronze → Silver (làm sạch/loại trùng)│
│  • Glue ETL Job 3: Silver → Gold (tổng hợp KPI)       │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  TẦNG TRUY VẤN                                         │
│  • Glue Data Catalog (registry metadata)               │
│  • Amazon Athena (SQL serverless trên S3)              │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  TẦNG TRỰC QUAN HÓA                                    │
│  • Streamlit Dashboard trên EC2 (trong VPC)            │
│  • Kết nối Athena qua aws-wrangler + boto3             │
└─────────────────────────────────────────────────────────┘
```

---

## Dịch vụ AWS Được Sử Dụng

| Dịch vụ | Vai trò trong Workshop |
|---------|------------------------|
| **Amazon VPC** | Mạng riêng biệt cho EC2 và nền tảng dữ liệu |
| **Public Subnet** | Subnet chứa EC2 Dashboard |
| **Internet Gateway** | Cho phép EC2 truy cập internet |
| **Route Table** | Định tuyến traffic từ subnet tới Internet Gateway |
| **Security Group** | Cho phép cổng 8501 (Streamlit) + SSH |
| **Amazon S3** | Data lake bốn tầng (Raw, Bronze, Silver, Gold) |
| **Amazon Data Firehose** | Đệm và gửi sự kiện streaming tới S3 |
| **Amazon API Gateway** | Điểm cuối HTTP để tiếp nhận sự kiện client |
| **AWS Lambda** | Chuyển đổi Firehose nội tuyến + trích xuất DB |
| **Amazon EventBridge Scheduler** | Kích hoạt batch Lambda theo lịch |
| **AWS Glue** | ETL job PySpark để chuyển đổi dữ liệu |
| **AWS Glue Data Catalog** | Registry metadata cho các bảng Athena |
| **Amazon Athena** | Truy vấn SQL serverless trên tầng Gold của S3 |
| **Amazon EC2** | Lưu trữ Streamlit dashboard |
| **Amazon EBS** | Lưu trữ persistent cho EC2 instance |
| **Elastic IP** | IP tĩnh cho EC2 instance |
| **AWS IAM** | Quyền hạn tối thiểu cho từng dịch vụ |
| **Amazon CloudWatch** | Log, metric và alarm |
| **AWS KMS** | Mã hóa at-rest cho S3 bucket |

---

## Các File Source Code

Toàn bộ source code sử dụng trong workshop này có trong thư mục `source_code/`:

| File | Mô tả |
|------|-------|
| `raw_to_bronze_job.py` | Glue ETL Job 1: Đọc CSV + JSON streaming từ Raw, ghi Parquet sang Bronze |
| `bronze_to_silver_job.py` | Glue ETL Job 2: Loại trùng, làm sạch, chuẩn hóa tên cột → Silver |
| `silver_to_gold_job.py` | Glue ETL Job 3: Tổng hợp KPI nghiệp vụ → Gold; tự động đăng ký bảng Glue Catalog |
| `athena_create_tables.sql` | SQL để tạo external table trong Athena (phương án thủ công) |
| `athena_queries.sql` | Các truy vấn nghiệp vụ mẫu để chạy trên tầng Gold |
| `app_beautiful.py` | Ứng dụng Streamlit dashboard kết nối Athena qua aws-wrangler |

---

## Kết quả Dashboard Cuối Cùng

Kết quả cuối cùng của workshop là một dashboard phân tích tương tác đầy đủ chạy trên EC2:

![Xu hướng Doanh thu](/result/DashBoard/Revenue%20Trend.png)

![Top Performers](/result/DashBoard/Top%20Performers.jpg)

![Phân phối Sự kiện](/result/DashBoard/Event%20Distribution.png)

---

## Thời gian & Chi phí Ước tính

| Mục | Giá trị |
|-----|---------|
| **Thời gian** | ~3–4 giờ (toàn bộ workshop) |
| **Chi phí ước tính** | ~$1–3 USD (nếu dọn dẹp trong ngày) |
| **AWS Region** | `us-east-1` (N. Virginia) - khuyến nghị |
| **Độ khó** | Trung cấp |

> 💡 **FinOps Tip:** Tổng chi phí được giữ thấp vì tất cả dịch vụ compute (Glue, Athena, Lambda, Firehose) đều trả theo mức sử dụng - bạn chỉ trả khi chúng chạy. EC2 instance (t3.micro) đủ điều kiện Free Tier trong 12 tháng đầu.

---

## Điều hướng

Tiến hành qua các phần theo thứ tự sau:

1. ✅ **5.1 Tổng quan** ← Bạn đang ở đây
2. → [5.2 Điều kiện tiên quyết](../5.2-Prerequisite/)
3. → [5.3 Mô tả Kiến trúc](../5.3-Architecture/)
4. → [5.4 Các bước thực hành](../5.4-Steps/)
5. → [5.5 Dọn dẹp tài nguyên](../5.5-Cleanup/)
