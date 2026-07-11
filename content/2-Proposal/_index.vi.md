---
title: "Bản đề xuất"
date: 2026-06-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# FinOps-Optimized Serverless Medallion Data Lakehouse Architecture for Customer Behavior Analytics

---

## 1. Tổng quan dự án

Bản đề xuất này trình bày thiết kế và triển khai end-to-end một **data lakehouse hoàn toàn serverless, thuần cloud** trên AWS - được xây dựng chuyên biệt cho bài toán phân tích hành vi khách hàng trong lĩnh vực thương mại điện tử. Nền tảng được đặt tên là **"FinOps-Optimized Serverless Medallion Data Lakehouse"** để phản ánh hai nguyên tắc thiết kế cốt lõi ăn sâu vào mọi quyết định kiến trúc:

1. **FinOps-first (Tối ưu chi phí là ưu tiên hàng đầu)**: Mỗi lựa chọn dịch vụ AWS đều được chọn nhằm tối thiểu hóa chi phí - serverless compute (không có chi phí idle), truy vấn theo yêu cầu, chuyển đổi dữ liệu trong chuyến bay để loại bỏ các lần ghi lưu trữ trung gian, và phân tầng lưu trữ S3 thông minh. Nền tảng mang lại khả năng phân tích cấp production với tổng chi phí ước tính dưới **$8/tháng** ở quy mô thực tập.

2. **Kiến trúc Medallion**: Dữ liệu thô chảy qua ba tầng S3 được tinh chỉnh dần - **Bronze** (vùng hạ cánh thô, bất biến) → **Silver** (đã làm sạch, xác thực schema) → **Gold** (đã tổng hợp theo nghiệp vụ, sẵn sàng phân tích) - đảm bảo chất lượng dữ liệu được cải thiện ở mỗi giai đoạn trong khi vẫn giữ khả năng phát lại toàn bộ pipeline từ dữ liệu thô bất kỳ lúc nào.

Nền tảng hợp nhất **hai luồng ingestion**: các sự kiện clickstream thời gian thực từ ứng dụng web và mobile (luồng streaming qua API Gateway → Firehose) và các bản ghi đơn hàng định kỳ từ cơ sở dữ liệu giao dịch (luồng batch qua EventBridge → Lambda). Cả hai luồng đều hạ vào cùng một S3 Bronze bucket, đảm bảo một nguồn sự thật duy nhất bất kể nguồn gốc dữ liệu. Downstream, các Glue ETL Job chuyển đổi dữ liệu qua các tầng Medallion, Amazon Athena cung cấp phân tích SQL serverless, và một **Streamlit Dashboard** trình bày các KPI sẵn sàng cho kinh doanh đến các bên liên quan.

> 📌 **Sơ đồ kiến trúc tổng thể:**

![FinOps-Optimized Serverless Medallion Data Lakehouse Architecture](/images/2-Proposal/Architecture_DE.png)

**Tổng quan nền tảng:**

| Chiều kích | Chi tiết |
|------------|---------|
| **Use case** | Phân tích hành vi khách hàng thương mại điện tử |
| **Ingestion** | Streaming thời gian thực (clickstream) + Batch theo lịch (đơn hàng) |
| **Pattern lưu trữ** | Kiến trúc Medallion: Bronze → Silver → Gold trên Amazon S3 |
| **Xử lý** | AWS Glue ETL (PySpark) - serverless, tính phí theo DPU-second |
| **Analytics** | Amazon Athena - SQL serverless, tính phí theo TB quét |
| **Trực quan hóa** | Python Streamlit Dashboard qua PyAthena |
| **IaC** | AWS CDK (TypeScript) - toàn bộ nền tảng được định nghĩa bằng code |
| **Chi phí ước tính** | ~$7–8/tháng ở quy mô thực tập |
| **Quản trị** | IAM quyền tối thiểu + KMS CMKs + CloudWatch observability |

---

## 2. Mục tiêu

Nền tảng được thiết kế để đạt được các mục tiêu có thể đo lường sau:

### 2.1. Mục tiêu kỹ thuật

**MT1 - Ingestion hai luồng hợp nhất:**
Xây dựng và xác thực hai luồng ingestion riêng biệt đều hạ vào một S3 Bronze bucket duy nhất:
- Luồng streaming: clickstream thời gian thực từ web/mobile → API Gateway → Firehose + Lambda → S3 Bronze, với xác thực tại biên dưới giây và chuyển đổi trong chuyến bay.
- Luồng batch: bản ghi đơn hàng giao dịch → EventBridge Scheduler → Lambda DB extractor (dựa trên watermark) → S3 Bronze, theo chu kỳ hàng giờ/hàng ngày có thể cấu hình.

**MT2 - Pipeline chất lượng dữ liệu Medallion ba tầng:**
Triển khai hai AWS Glue ETL Job tuần tự tinh chỉnh dần chất lượng dữ liệu:
- **Glue ETL Job 1 (Bronze → Silver)**: loại bỏ trùng lặp, xử lý null, thực thi schema, chuyển đổi kiểu, chuyển sang Parquet với nén Snappy.
- **Glue ETL Job 2 (Silver → Gold)**: tổng hợp KPI nghiệp vụ - doanh thu hàng ngày theo danh mục, tỉ lệ chuyển đổi phễu người dùng, phân khúc LTV khách hàng, chỉ số hiệu suất sản phẩm.

**MT3 - Phân tích SQL serverless với tối ưu hóa FinOps:**
Cấu hình Amazon Athena với Workgroup chuyên dụng thực thi giới hạn quét dữ liệu mỗi truy vấn, kết hợp định dạng cột Parquet và phân vùng kiểu Hive để giảm dữ liệu quét hiệu quả 85–90% so với JSON thô - mang lại hiệu suất truy vấn dưới giây trên dữ liệu tầng Gold với chi phí tối thiểu.

**MT4 - Streamlit Dashboard tương tác:**
Phát triển ứng dụng web Python Streamlit kết nối với Athena qua `pyathena` hiển thị ít nhất 5 KPI nghiệp vụ (phễu bán hàng, xu hướng doanh thu, bảng xếp hạng sản phẩm, phân tích cohort khách hàng, luồng sự kiện gần thời gian thực) với cache kết quả 5 phút để tối thiểu chi phí truy vấn lặp lại.

**MT5 - Infrastructure as Code (IaC):**
Định nghĩa toàn bộ nền tảng - S3 buckets, IAM roles, KMS keys, tài nguyên Glue, API Gateway, Lambda, Firehose, EventBridge, Athena Workgroup - dưới dạng CDK TypeScript constructs, cho phép deploy một lệnh (`cdk deploy`) và xóa (`cdk destroy`) có thể lặp lại.

**MT6 - Quản trị và khả năng quan sát:**
Triển khai IAM roles quyền tối thiểu theo từng dịch vụ, AWS KMS Customer Managed Keys theo tầng S3, và CloudWatch Dashboard với alarms bao phủ tỉ lệ lỗi Lambda, lỗi Glue Job, throttling Firehose và timeout truy vấn Athena.

### 2.2. Mục tiêu học tập

Ngoài các deliverable kỹ thuật, dự án này là trải nghiệm học tập thực hành trong thực tập để phát triển năng lực:

| Lĩnh vực kỹ năng | Dịch vụ AWS / Công cụ |
|-----------------|----------------------|
| Serverless compute | AWS Lambda, Amazon API Gateway |
| Streaming ingestion | Amazon Data Firehose |
| Batch orchestration | Amazon EventBridge Scheduler |
| Lưu trữ data lake | Amazon S3, Parquet, nén Snappy |
| ETL & data engineering | AWS Glue PySpark, Glue Data Catalog |
| SQL analytics | Amazon Athena, tối ưu hóa truy vấn |
| Bảo mật & quản trị | AWS IAM, AWS KMS, CloudTrail |
| Infrastructure as Code | AWS CDK (TypeScript) |
| Trực quan hóa dữ liệu | Python Streamlit, PyAthena, Pandas |
| FinOps / tối ưu chi phí | S3 lifecycle, Athena Workgroup, định dạng cột Parquet |

---

## 3. Vấn đề cần giải quyết

### 3.1. Bối cảnh kinh doanh

Các doanh nghiệp thương mại điện tử hiện đại tạo ra khối lượng dữ liệu khổng lồ mỗi giây - từ các sự kiện clickstream thời gian thực trên website và ứng dụng di động (xem trang, click sản phẩm, thêm vào giỏ hàng, hoàn tất thanh toán) đến các bản ghi đơn hàng giao dịch được lưu trong cơ sở dữ liệu quan hệ backend. Khi được khai thác đúng cách, dữ liệu này mở ra những insight mạnh mẽ về pattern hành vi khách hàng, tỉ lệ chuyển đổi phễu bán hàng, hiệu suất sản phẩm và hiệu quả vận hành.

Tuy nhiên, đối với các team thương mại điện tử nhỏ đến trung bình (và các dự án quy mô thực tập hoạt động trên AWS credits có giới hạn), việc tiếp cận những insights này bị cản trở bởi một tập hợp thách thức hạ tầng liên kết với nhau:

### 3.2. Năm vấn đề cốt lõi

**Vấn đề 1 - Tốc độ dữ liệu kép không có vùng hạ cánh hợp nhất**

Các sự kiện clickstream đến liên tục ở tốc độ biến đổi (0 đến hàng nghìn sự kiện/giây), yêu cầu ingestion streaming thông lượng cao độ trễ thấp. Các bản ghi đơn hàng, ngược lại, được tạo bởi cơ sở dữ liệu OLTP giao dịch không thể truy vấn liên tục mà không làm giảm hiệu suất production - yêu cầu pattern trích xuất batch có lịch trình.

Không có nền tảng xử lý cả hai, các team buộc phải chọn: xây dựng hai pipeline riêng với lưu trữ riêng, hoặc đưa tất cả về batch và bỏ mất tín hiệu hành vi thời gian thực.

**Vấn đề 2 - Suy giảm chất lượng dữ liệu không có lớp thực thi**

Các payload sự kiện do client tạo ra vốn không đáng tin cậy: chúng có thể chứa JSON không hợp lệ, thiếu trường bắt buộc, kiểu dữ liệu không hợp lệ, event ID trùng lặp (từ retry logic của client) hoặc timestamp lỗi thời. Không có lớp xác thực và chuyển đổi, những lỗi này lan truyền âm thầm vào phân tích downstream - làm hỏng KPIs, phóng đại số lượng người dùng và tạo ra các quyết định kinh doanh sai lệch.

**Vấn đề 3 - Căng thẳng chi phí vs. quy mô với các approach truyền thống**

Các giải pháp analytics truyền thống cho use case này (ví dụ: cluster Redshift luôn chạy, cluster EMR chạy liên tục, Kafka broker cố định) phát sinh chi phí cố định đáng kể bất kể khối lượng truy vấn hay xử lý thực tế. Với ngân sách AWS credit có hạn và workload biến đổi cao (thấp ban đêm, cao trong giờ kinh doanh), mô hình chi phí cố định này là không bền vững về kinh tế.

| Approach truyền thống | Chi phí ước tính/tháng | Vấn đề |
|----------------------|----------------------|--------|
| Amazon Redshift (ra3.xlplus, 2 nodes) | ~$700–900/tháng | Over-provisioning khổng lồ cho quy mô thực tập |
| Amazon EMR (m5.xlarge, 3 nodes) | ~$300–500/tháng | Chi phí cluster idle giữa các lần chạy batch |
| Amazon MSK (kafka.m5.large, 3 brokers) | ~$400–600/tháng | Chi phí 24/7 ngay cả khi không có event nào đang chảy |
| **Nền tảng này (hoàn toàn serverless)** | **~$7–8/tháng** | **Chỉ trả tiền cho mức sử dụng thực tế** |

**Vấn đề 4 - Không có quản trị hay kiểm soát truy cập tập trung**

Không có nền tảng có cấu trúc, các kỹ sư dữ liệu có xu hướng áp dụng S3 bucket policies và IAM permissions một cách ad-hoc - dẫn đến "permission sprawl" khi các dịch vụ tích lũy nhiều quyền truy cập hơn mức cần thiết. Dữ liệu khách hàng nhạy cảm (địa chỉ email, lịch sử mua hàng, hồ sơ hành vi) trở nên có thể truy cập bởi bất kỳ thành viên nào trong team hoặc dịch vụ nào có quyền đọc S3, vi phạm nguyên tắc quyền tối thiểu và tạo ra rủi ro tuân thủ.

**Vấn đề 5 - Không có quản lý schema hay tối ưu hóa truy vấn**

Dữ liệu JSON thô được lưu trong S3 không có catalog schema liên quan, khiến các công cụ SQL như Athena không thể hiểu cấu trúc bảng mà không có câu lệnh `CREATE TABLE` thủ công. Ngoài ra, truy vấn JSON thô bằng Athena đắt hơn đáng kể so với truy vấn Parquet (Athena tính phí theo TB quét - file JSON có kích thước lớn hơn 5–10 lần so với file Parquet tương đương cho cùng dữ liệu logic).

### 3.3. Tại sao điều này quan trọng

Không giải quyết năm vấn đề này, khả năng phân tích thương mại điện tử vẫn:
- **Không tồn tại** (không có nền tảng nào được xây dựng) - quyết định kinh doanh dựa trên cảm tính, không dựa trên dữ liệu
- **Không vững chắc** (script ad-hoc, SQL thủ công) - không thể tái tạo, không thể mở rộng, không được quản trị
- **Đắt đỏ** (cluster luôn chạy) - không bền vững trên AWS credits quy mô thực tập

Bản đề xuất này giải quyết đồng thời cả năm vấn đề thông qua một data lakehouse serverless, được định nghĩa bằng IaC, nhất quán, vừa tiết kiệm chi phí vừa sẵn sàng cho production.

---

## 4. Kiến trúc giải pháp

### 4.1. Tổng quan kiến trúc

Nền tảng được tổ chức thành **sáu lớp chức năng** cộng với một **lớp quản trị nằm ngang**, mỗi lớp có trách nhiệm được xác định chính xác:

| Lớp | Dịch vụ AWS | Trách nhiệm |
|-----|------------|------------|
| **Data Source** | Website, Mobile App, E-commerce Orders DB | Tạo sự kiện và bản ghi giao dịch |
| **Ingestion Layer** | API Gateway, Data Firehose, Lambda, EventBridge Scheduler | Thu thập dữ liệu hai luồng và xác thực tại biên |
| **Storage Layer** | Amazon S3 (Bronze / Silver / Gold) | Lưu trữ data lake bất biến theo tầng Medallion |
| **Processing Layer** | AWS Glue ETL Jobs, Glue Data Catalog | Chuyển đổi schema và tổng hợp nghiệp vụ |
| **Query Layer** | Amazon Athena, Glue Data Catalog | Phân tích SQL serverless trên S3 |
| **Visualization Layer** | Streamlit Dashboard | Khám phá KPI nghiệp vụ tương tác |
| **Governance** | AWS IAM, AWS KMS, Amazon CloudWatch | Bảo mật, mã hóa và khả năng quan sát |

---

### 4.2. Nguồn dữ liệu (Data Sources)

**Nguồn 1 - Website & Ứng dụng di động (Sự kiện thời gian thực)**

Các ứng dụng web và mobile hướng đến người dùng liên tục phát ra các sự kiện hành vi - xem trang, xem chi tiết sản phẩm, thêm vào giỏ hàng, khởi tạo thanh toán, hoàn tất mua hàng và kết thúc phiên. Mỗi sự kiện là một payload JSON có cấu trúc được gửi qua HTTP POST đến endpoint ingestion. Khối lượng biến đổi cao: gần bằng không lúc 3 giờ sáng, đạt đỉnh trong các đợt flash sale.

- **Định dạng**: JSON, phiên bản schema theo loại sự kiện
- **Tốc độ**: 0 đến hàng nghìn sự kiện/giây (không thể đoán trước)
- **Yêu cầu độ trễ**: Ingestion dưới giây; phân tích chấp nhận được trong vài phút
- **Rủi ro chất lượng**: JSON không hợp lệ, trường bắt buộc bị thiếu, kiểu dữ liệu sai từ bug client

**Nguồn 2 - Cơ sở dữ liệu đơn hàng (Bản ghi Batch)**

Một cơ sở dữ liệu quan hệ giao dịch (PostgreSQL/MySQL) lưu trữ các bản ghi đơn hàng hoàn thành bao gồm order ID, customer ID, SKU, số lượng, giá, trạng thái thanh toán và timestamp hoàn tất. Không thể truy vấn liên tục mà không làm giảm hiệu suất OLTP production.

- **Định dạng**: Hàng quan hệ → được trích xuất thành Apache Parquet
- **Tốc độ**: Batch, trích xuất hàng giờ hoặc hàng ngày
- **Yêu cầu độ trễ**: T+1 giờ là chấp nhận được
- **Rủi ro chất lượng**: Bản ghi trùng lặp từ retry logic; cập nhật một phần từ giao dịch chạy lâu

---

### 4.3. Lớp tiếp nhận dữ liệu (Ingestion Layer)

**Luồng A - Web / Mobile Streaming** *(Bước 1 → 2 → 3)*

**Bước 1 - Amazon API Gateway: Ingestion tại biên & Xác thực**

Tất cả sự kiện client đi vào qua HTTP POST endpoint trên **Amazon API Gateway** (REST API). Một **Request Validator** thực thi **JSON Schema** chặt chẽ tại biên - các request không hợp lệ bị từ chối ngay lập tức với `400 Bad Request` trước khi đến bất kỳ dịch vụ downstream nào.

> **Tác động FinOps**: Xác thực tại API Gateway không phát sinh thêm chi phí - dữ liệu xấu bị từ chối trước khi Lambda hay Firehose được gọi, ngăn ngừa compute downstream lãng phí.

**Bước 2 - Amazon Data Firehose + AWS Lambda: Đệm & Chuyển đổi nội tuyến**

Các payload đã xác thực chảy vào luồng phân phối **Amazon Data Firehose**. Firehose được chọn thay vì Kinesis Data Streams vì không cần lập kế hoạch shard capacity, tự nhiên đệm và batch records trước khi phân phối S3, và hỗ trợ gọi Lambda đồng bộ nội tuyến.

Firehose gọi đồng bộ **AWS Lambda** nhẹ (128 MB RAM) để chuyển đổi trong chuyến bay:
- Chuẩn hóa timestamp sự kiện sang UTC ISO-8601
- Làm phong phú records với pipeline metadata
- Xác thực mềm trường thứ cấp (đánh dấu bất thường không xóa records)
- Trả về records đã chuyển đổi **trong bộ nhớ** - không có lần ghi S3 trung gian nào

> **Tác động FinOps**: Chuyển đổi Lambda trong RAM loại bỏ vòng PUT+GET S3 trung gian mà các pipeline truyền thống "ghi rồi đọc" phải chịu.

**Bước 3 - S3 Bronze Bucket: Điểm đến Streaming**

Firehose flush các records đã đệm dưới dạng **NDJSON**, được phân vùng theo:
```
s3://[project]-bronze/events/year=YYYY/month=MM/day=DD/hour=HH/
```

Bronze bucket là **thô và bất biến** - dữ liệu được lưu giữ chính xác như nhận, đóng vai trò là nguồn sự thật duy nhất để tái xử lý toàn bộ pipeline.

---

**Luồng B - Đồng bộ DB / Batch** *(Bước 8 → Lambda → S3 Bronze)*

**Bước 8 - Amazon EventBridge Scheduler: Trigger điều phối**

Một quy tắc **EventBridge Scheduler** kích hoạt theo biểu thức cron (ví dụ: `rate(1 hour)`). Không có cơ sở hạ tầng nào luôn chạy - không có EC2, không có container, không có tiến trình liên tục. Chi phí chỉ phát sinh trong cửa sổ thực thi.

**AWS Lambda - Hàm trích xuất DB**

Trigger gọi một **Lambda function** thực hiện:
1. Lấy DB credentials từ **AWS Secrets Manager** (không bao giờ hardcode)
2. Truy vấn records sử dụng **watermark pattern**: `WHERE updated_at > last_successful_run_timestamp`
3. Chuyển đổi tập kết quả thành **Apache Parquet** trong bộ nhớ bằng PyArrow
4. Ghi file Parquet vào S3 Bronze dưới prefix được phân tách logic:
```
s3://[project]-bronze/orders/year=YYYY/month=MM/day=DD/batch_id=UUID/
```
5. Lưu watermark timestamp mới vào **AWS SSM Parameter Store** để re-run idempotent

---

### 4.4. Lớp lưu trữ (Storage Layer) - Kiến trúc Medallion

Nền tảng triển khai **Kiến trúc Medallion** - mỗi tầng S3 đại diện cho mức độ chất lượng và sẵn sàng cho nghiệp vụ ngày càng cao hơn:

| Tầng | S3 Bucket | Định dạng | Phân vùng | Mô tả |
|------|-----------|-----------|-----------|-------|
| **Bronze** | `[proj]-bronze` | NDJSON (stream) / Parquet (batch) | `year/month/day/hour` | Thô, bất biến. Luôn có thể tái xử lý đầy đủ từ đây. |
| **Silver** | `[proj]-silver` | Parquet + Snappy | `year/month/day` | Đã làm sạch, loại bỏ trùng lặp, xác thực schema. Tối ưu cho truy vấn. |
| **Gold** | `[proj]-gold` | Parquet + Snappy | `metric_date/category` | KPI đã tổng hợp trước. Được tiêu thụ trực tiếp bởi lớp trực quan hóa. |

**Tại sao Parquet + Snappy?**
- Giảm lưu trữ lên đến **87%** so với JSON thô → chi phí S3 thấp hơn
- **Column pruning**: Athena chỉ đọc cột được truy cập → ít dữ liệu quét hơn → chi phí truy vấn thấp hơn
- **Predicate pushdown**: Athena bỏ qua row groups không khớp bộ lọc WHERE → nhanh hơn và rẻ hơn

**Ví dụ Gold datasets được tạo ra:**
- `daily_revenue_by_category` - doanh thu theo danh mục sản phẩm và ngày
- `user_funnel_daily` - số lượng người dùng ở mỗi giai đoạn phễu (view → cart → checkout → purchase)
- `customer_ltv_segments` - giá trị vòng đời khách hàng tích lũy 90 ngày được phân nhóm thành các tier LTV
- `product_performance_weekly` - tỉ lệ chuyển đổi view thành mua theo sản phẩm, trailing 7 ngày

**Bảo mật:** Cả ba bucket được mã hóa khi lưu trữ bằng **AWS KMS Customer Managed Keys (CMKs)** - một CMK riêng cho mỗi tầng. S3 bucket policies thực thi quyền ghi xuyên tầng bằng không.

---

### 4.5. Lớp xử lý (Processing Layer) - Pipeline AWS Glue ETL

**Glue ETL Job 1 - Chuyển đổi Bronze → Silver (Bước 5)**

Được trigger bởi EventBridge sau khi batch ingestion hoàn thành. Đọc từ Bronze, áp dụng:
1. **Thực thi schema** - cast trường sang kiểu dữ liệu canonical
2. **Loại bỏ trùng lặp** - window function trên `event_id` / `order_id`, giữ lần gần nhất
3. **Xử lý null** - điền optional nulls với defaults; cách ly records thiếu trường bắt buộc sang prefix `_quarantine/`
4. **Chuẩn hóa chuỗi** - chữ thường cho danh mục, chuẩn hóa định dạng điện thoại/email
5. **Chuyển đổi định dạng** - output Parquet + Snappy, phân vùng theo `year/month/day`

Khi hoàn thành: gọi Glue Data Catalog API để đăng ký partition Silver mới - **không cần Crawler**.

**Glue ETL Job 2 - Tổng hợp Silver → Gold (Bước 6)**

Chạy sau Job 1. Đọc từ Silver, tính toán:
1. Tổng hợp doanh thu: `SUM(order_total) GROUP BY (category, order_date)`
2. Phân tích phễu: số lượng user riêng biệt theo `event_type` theo ngày + tỉ lệ chuyển đổi giai đoạn
3. Phân khúc LTV khách hàng: tổng chi tiêu tích lũy 90 ngày theo `customer_id` → nhãn phân khúc LTV
4. Hiệu suất sản phẩm: tỉ lệ view-to-purchase theo `product_id` trong cửa sổ trailing 7 ngày
5. Tái tạo phiên: nhóm clickstream events thành phiên (khoảng trống không hoạt động 30 phút) → tính thời gian phiên và số trang/phiên

Khi hoàn thành: đăng ký partition bảng Gold trong Glue Data Catalog.

**Glue Data Catalog (Bước 7)**

Kho siêu dữ liệu trung tâm cho cả ba tầng. Lưu trữ schemas bảng, khóa phân vùng và vị trí vật lý S3. Cả hai ETL Job đều đăng ký output trực tiếp qua Catalog API - **không có Crawler định kỳ**, loại bỏ chi phí DPU-hour của crawl theo lịch. Amazon Athena đọc từ Catalog để lập kế hoạch thực thi truy vấn tối ưu mà không cần di chuyển dữ liệu.

---

### 4.6. Lớp truy vấn (Query Layer) - Amazon Athena

Amazon Athena cung cấp **phân tích SQL tương tác, serverless** trực tiếp trên dữ liệu S3 - không có cluster, không có provisioning, chỉ trả tiền theo TB quét.

**Stack tối ưu hóa FinOps cho Athena:**

| Tối ưu hóa | Cơ chế | Tác động chi phí |
|-----------|--------|----------------|
| Định dạng cột Parquet | Silver + Gold lưu dưới dạng Parquet | Giảm 70–90% dữ liệu quét so với JSON |
| Nén Snappy | Tất cả file Parquet được nén | Object S3 nhỏ hơn → ít dữ liệu truyền hơn |
| Phân vùng Hive | Khóa phân vùng `year/month/day` | Athena loại bỏ partition không liên quan trước khi quét |
| Tầng Gold tổng hợp trước | Truy vấn dashboard nhắm vào Gold | Quét hàng nghìn hàng vs. hàng triệu sự kiện thô |
| Tái sử dụng kết quả truy vấn | Caching kết quả Athena được bật | Truy vấn giống nhau trong 24h trả về kết quả cached với $0 |
| Giới hạn quét Workgroup | Giới hạn quét mỗi truy vấn (ví dụ: tối đa 1 GB) | Ngăn truy vấn chạy quá mức tiêu thụ credits |

Athena được truy cập theo chương trình bởi Streamlit qua `pyathena` (giao diện DBAPI2) với SQL tham số hóa. Kết quả được lưu trong S3 results bucket chuyên dụng để audit trails và caching.

---

### 4.7. Lớp trực quan hóa (Visualization Layer) - Streamlit Dashboard

Một **ứng dụng web Python Streamlit** kết nối với Athena qua `pyathena` và hiển thị dữ liệu tầng Gold dưới dạng biểu đồ nghiệp vụ tương tác và thẻ KPI.

**Các khả năng Dashboard:**

| View | Mô tả |
|------|-------|
| **Phễu bán hàng** | Biểu đồ Sankey/phễu: drop-off view → cart → checkout → purchase theo loại thiết bị |
| **Xu hướng doanh thu** | Biểu đồ đường time-series: doanh thu hàng ngày/hàng tuần theo danh mục sản phẩm |
| **Cohort khách hàng** | Retention heatmap: tháng acquisition nào tạo ra nhiều khách hàng trung thành nhất? |
| **Bảng xếp hạng sản phẩm** | Bảng có thể sắp xếp: top sản phẩm theo lượt xem, tỉ lệ thêm giỏ hàng và doanh thu |
| **Luồng sự kiện gần thời gian thực** | Các sự kiện mới nhất từ Bronze được poll qua Athena |

**Pattern caching kết quả (FinOps):**
```python
@st.cache_data(ttl=300)  # cache trong 5 phút
def load_daily_revenue(start_date, end_date):
    # Athena chỉ được truy vấn một lần mỗi 5 phút
    # Tương tác dashboard lặp lại trong cửa sổ này: chi phí Athena $0
    return pd.read_sql(query, conn, params=[start_date, end_date])
```

**Hosting:** EC2 t3.micro (trong Free Tier) hoặc AWS App Runner, được deploy trong cùng VPC với nền tảng dữ liệu để kết nối riêng tư đến Athena/S3 mà không cần internet công cộng.

---

### 4.8. Quản trị, Bảo mật & Giám sát

**IAM - IAM Roles quyền tối thiểu**

| Dịch vụ | Quyền IAM (có phạm vi) |
|---------|----------------------|
| Lambda (Ingestion) | `firehose:PutRecord` chỉ trên Firehose stream cụ thể |
| Lambda (DB Extractor) | `s3:PutObject` Bronze prefix `/orders/` + `secretsmanager:GetSecretValue` ARN cụ thể |
| Glue ETL Job 1 | `s3:GetObject` Bronze + `s3:PutObject` Silver + `glue:UpdateTable` chỉ bảng Silver |
| Glue ETL Job 2 | `s3:GetObject` Silver + `s3:PutObject` Gold + `glue:UpdateTable` chỉ bảng Gold |
| Athena | `s3:GetObject` Silver+Gold + `s3:PutObject` results bucket + `glue:GetTable/GetPartitions` |
| Streamlit | `athena:StartQueryExecution`, `athena:GetQueryResults`, `s3:GetObject` chỉ results |

Không có quyền wildcard `s3:*` ở bất kỳ đâu. Quyền ghi xuyên tầng là không thể về mặt kiến trúc.

**KMS - Mã hóa phong bì theo tầng**

Ba Customer Managed Keys (CMKs) riêng biệt:
- `finops/bronze-cmk` → mã hóa Bronze bucket
- `finops/silver-cmk` → mã hóa Silver bucket
- `finops/gold-cmk` → mã hóa Gold bucket

Tất cả sự kiện sử dụng key được ghi vào CloudTrail → CloudWatch Logs để audit trail chống giả mạo.

**CloudWatch - Khả năng quan sát pipeline**

*Alarms:*
| Alarm | Metric | Ngưỡng | Cảnh báo |
|-------|--------|--------|---------|
| Tỉ lệ lỗi Lambda | `Errors/Invocations` | > 5% / 5 phút | SNS email |
| Lỗi Glue Job | `numFailedTasks` | > 0 | SNS email |
| Throttling Firehose | `ThrottledRecords` | > 100/phút | SNS email |
| Timeout truy vấn Athena | `QueryExecutionTime` | > 60s | CloudWatch log |

*CloudWatch Dashboard hợp nhất:* tỉ lệ gọi Lambda, tiêu thụ DPU Glue, số truy vấn Athena/ngày, dữ liệu quét/ngày, tăng trưởng lưu trữ S3 theo tầng - tất cả trong một chế độ xem vận hành.

---

## 5. Timeline

| Giai đoạn | Thời gian | Deliverables chính |
|-----------|-----------|-------------------|
| **Giai đoạn 1 - Thiết kế kiến trúc & IaC Scaffolding** | Tuần 1–2 | CDK stack: S3 buckets (×3), IAM roles (×6), KMS CMKs (×3), Glue Data Catalog, cấu hình VPC |
| **Giai đoạn 2 - Streaming Ingestion (Luồng A)** | Tuần 3–4 | API Gateway REST API + JSON Schema validator; Firehose delivery stream; Lambda transformation (128 MB, in-flight Snappy); kiểm thử end-to-end: POST event → Bronze S3 xác minh |
| **Giai đoạn 3 - Batch Ingestion (Luồng B)** | Tuần 5 | EventBridge Scheduler rule; Lambda DB extractor với watermark logic + SSM Parameter Store; chuyển đổi Parquet với PyArrow; Bronze xác minh cho cả hai prefix streaming và batch |
| **Giai đoạn 4 - Lớp Glue ETL Processing** | Tuần 6–7 | Glue ETL Job 1: deduplication + schema enforcement + Silver Parquet output + Catalog registration; Glue ETL Job 2: KPI aggregations + Gold output + Catalog registration; pipeline run end-to-end được xác minh |
| **Giai đoạn 5 - Query Layer & Dashboard** | Tuần 8–9 | Athena Workgroup với cost controls; truy vấn bảng Gold tier được xác minh; Streamlit Dashboard với tất cả 5 KPI views hoạt động; kết nối PyAthena với cache 5 phút |
| **Giai đoạn 6 - Quản trị & Hardening** | Tuần 10 | KMS CMK theo tầng được thực thi; scan IAM Access Analyzer; CloudWatch Alarms + Dashboard hoạt động; smoke test đầy đủ end-to-end từ event thô → Streamlit chart |

**Tổng thời gian: 10 tuần** (phù hợp với kỳ thực tập FCJ Data Engineer)

**Các mốc kiểm tra:**

```
Tuần 2  ──► Nền tảng IaC hoàn thành (cdk deploy chạy không có lỗi)
Tuần 4  ──► Sự kiện thực đầu tiên đến S3 Bronze qua luồng streaming
Tuần 5  ──► Bản ghi đơn hàng batch đầu tiên hạ xuống S3 Bronze qua DB sync
Tuần 7  ──► Pipeline đầy đủ Bronze → Silver → Gold chạy end-to-end
Tuần 9  ──► Streamlit Dashboard hiển thị KPI tầng Gold trực tiếp
Tuần 10 ──► Nền tảng được hardened, giám sát và tài liệu hóa
```

---

## 6. Ngân sách

Kiến trúc được thiết kế để duy trì dưới **$10/tháng** ở quy mô thực tập (~100.000 sự kiện/ngày, ~1 GB/ngày được ingested, 2 lần chạy Glue job/ngày, ~50 truy vấn Athena/ngày).

| # | Dịch vụ | Ước tính sử dụng | Chi phí/tháng |
|---|---------|----------------|--------------|
| 1 | Amazon API Gateway | 3 triệu request/tháng | ~$3.50 |
| 2 | Amazon Data Firehose | 1 GB/ngày × 30 = 30 GB | ~$0.90 |
| 3 | AWS Lambda | ~150K gọi, 128 MB, avg 500ms | **$0.00** (Free Tier: 1 triệu req/tháng) |
| 4 | Amazon EventBridge Scheduler | 60 gọi/tháng | **$0.00** (Free Tier: 14 triệu/tháng) |
| 5 | Amazon S3 (3 buckets) | ~30 GB tổng lưu trữ | ~$0.69 |
| 6 | AWS Glue ETL Jobs | 2 jobs × 2 DPUs × 30 phút × 30 ngày | ~$0.88 |
| 7 | AWS Glue Data Catalog | < 1 triệu objects | **$0.00** (Free Tier) |
| 8 | Amazon Athena | ~10 GB quét/tháng (Parquet tối ưu) | **~$0.05** |
| 9 | Amazon CloudWatch | Metrics mặc định + 5 custom alarms | ~$0.30 |
| 10 | AWS KMS | 3 CMKs + ~10K API calls | ~$0.30 |
| 11 | AWS Secrets Manager | 1 secret | ~$0.40 |
| | **Tổng** | | **~$7.02/tháng** |

> **Ghi chú FinOps về chi phí Athena:** Nếu không có Parquet và phân vùng, truy vấn cùng 30 GB dữ liệu JSON thô sẽ tốn khoảng **$0.15/TB × 30 GB/ngày × 30 ngày = ~$1.35/tháng** - tăng chi phí 27 lần so với $0.05/tháng tối ưu hóa. Parquet + phân vùng là tối ưu hóa có ROI cao nhất trong kiến trúc này.

**Phạm vi AWS Free Tier:** Lambda, EventBridge Scheduler và Glue Data Catalog hoàn toàn nằm trong AWS Free Tier ở quy mô thực tập - ba dịch vụ then chốt với chi phí hiệu quả $0.

Xem chi tiết ước tính chi phí tại [AWS Pricing Calculator](https://calculator.aws).

---

## 7. Rủi ro

### 7.1. Ma trận rủi ro

| # | Rủi ro | Xác suất | Tác động | Mức độ |
|---|--------|----------|---------|--------|
| R1 | Lambda timeout trong chuyển đổi nội tuyến Firehose (payload quá lớn / xử lý quá chậm) | Thấp | Trung bình | **Trung bình** |
| R2 | Vượt chi phí DPU Glue ETL Job từ dataset lớn bất ngờ | Trung bình | Trung bình | **Trung bình** |
| R3 | Đột biến chi phí quét Athena từ full-table scan vô tình trên Bronze hoặc Silver | Thấp | Cao | **Cao** |
| R4 | Mất dữ liệu S3 Bronze (xóa vô tình hoặc cấu hình bucket sai) | Rất thấp | Nghiêm trọng | **Cao** |
| R5 | Watermark drift của DB extractor gây bản ghi trùng lặp hoặc bị bỏ qua | Trung bình | Trung bình | **Trung bình** |
| R6 | Cấu hình sai IAM cấp quyền ghi xuyên tầng | Thấp | Cao | **Cao** |
| R7 | Firehose delivery failures gây mất dữ liệu trong quá trình truyền | Thấp | Trung bình | **Trung bình** |
| R8 | Khối lượng truy vấn Streamlit Dashboard gây chi phí Athena ngoài dự kiến | Trung bình | Thấp | **Thấp** |

### 7.2. Chiến lược giảm thiểu

**R1 - Lambda Timeout trong Firehose Transformation**
- Đặt Firehose Lambda timeout 60 giây (nằm trong giới hạn tối đa 5 phút của Firehose)
- Giữ Lambda memory ở 128 MB; profile logic chuyển đổi để đảm bảo hoàn thành trong < 10 giây mỗi batch
- Triển khai **soft-fail pattern**: nếu Lambda trả về lỗi, Firehose fallback giao bản ghi gốc (chưa chuyển đổi) thay vì xóa - ngăn mất dữ liệu với chi phí là cờ chất lượng dữ liệu downstream

**R2 - Vượt chi phí DPU Glue ETL Job**
- Đặt giới hạn `MaxCapacity` trong cấu hình Glue job (ví dụ: tối đa 4 DPUs mỗi lần chạy)
- Bật **Glue Job Bookmarks** để chỉ xử lý partition mới kể từ lần chạy thành công cuối - ngăn full re-scan mỗi trigger
- Giám sát `glue.driver.jvm.heap.usage` qua CloudWatch; đặt alarm nếu DPU-hours vượt ngưỡng ngân sách
- Cân nhắc **Glue Serverless (Flex)** execution class cho các job không khẩn cấp - rẻ hơn tới 34% so với standard

**R3 - Đột biến chi phí quét Athena**
- Thực thi **giới hạn quét dữ liệu mỗi truy vấn** qua Athena Workgroup (ví dụ: tối đa 1 GB) - bất kỳ truy vấn nào vượt qua bị tự động hủy trước khi quét hoàn thành
- Tất cả truy vấn dashboard **phải** nhắm vào tầng Gold; Silver và Bronze chỉ được truy cập trong debug ad-hoc bởi kỹ sư được ủy quyền
- Bật **tái sử dụng kết quả truy vấn Athena** - các truy vấn SQL giống nhau trong 24h trả về kết quả cached với chi phí quét $0 bổ sung
- Dùng `@st.cache_data(ttl=300)` trong Streamlit để ngăn việc re-execute truy vấn mỗi tương tác người dùng

**R4 - Mất dữ liệu S3 Bronze**
- Bật **S3 Versioning** trên Bronze bucket - bất kỳ `DeleteObject` vô tình nào tạo delete marker, cho phép khôi phục về bất kỳ version trước đó nào
- Bật **S3 Object Lock** (Governance mode) với thời gian giữ lại 30 ngày trên Bronze objects - ngăn xóa bởi bất kỳ IAM principal nào (kể cả admin) trong 30 ngày
- Cân nhắc **Cross-Region Replication** cho production: tự động sao chép Bronze objects sang region AWS thứ hai như bản sao disaster recovery

**R5 - Watermark Drift của DB Extractor**
- Lưu watermark timestamp vào **AWS SSM Parameter Store** với atomic writes - nếu Lambda thất bại giữa chừng, watermark không được advance, đảm bảo lần chạy tiếp theo tái xử lý cửa sổ thất bại
- Dùng **`batch_id=UUID`** làm khóa phân vùng trong Bronze cho tất cả batch writes - cho phép Glue ETL Job 1 dùng deduplication dựa trên batch_id ngay cả khi cùng records được trích xuất hai lần
- Triển khai **reconciliation check**: sau mỗi lần trích xuất, đếm records được trích xuất và so sánh với `SELECT COUNT(*)` trên DB cho cùng cửa sổ thời gian; ghi log sai lệch

**R6 - Cấu hình sai IAM**
- Tất cả IAM roles được định nghĩa độc quyền trong **AWS CDK IaC** - không cho phép thay đổi console thủ công; quyền role được version-controlled trong Git
- Chạy **AWS IAM Access Analyzer** hàng tuần để tự động đánh dấu bất kỳ resource-based policies nào cấp quyền rộng hơn dự định
- Không IAM role nào có `"Action": "*"` hay `"Resource": "*"` - được thực thi bởi quy tắc CDK `NagPack` thất bại `cdk synth` nếu phát hiện quyền wildcard

**R7 - Firehose Delivery Failures**
- Bật **S3 backup** tích hợp của Firehose cho records thất bại - bất kỳ record nào Firehose không thể giao đến đích chính được tự động ghi vào prefix `_failed/` S3 riêng để điều tra thủ công
- Đặt **CloudWatch Alarm** trên metric `DeliveryToS3.DataFreshness` - cảnh báo nếu dữ liệu được đệm trong Firehose lâu hơn 15 phút (cho thấy có tắc nghẽn phân phối)

**R8 - Chi phí Truy vấn Streamlit Dashboard**
- Triển khai `@st.cache_data(ttl=300)` trên tất cả hàm truy vấn Athena - giới hạn Athena invocations còn một lần mỗi 5 phút cho mỗi query signature duy nhất
- Cấu hình Athena Workgroup với **ngân sách quét dữ liệu hàng tháng theo workgroup** với SNS alert ở 80% ngân sách - cảnh báo chủ động trước khi vượt chi phí xảy ra
