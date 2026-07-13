---
title: "Điều kiện tiên quyết"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 5.2 </b> "
---

# Điều kiện tiên quyết

Trước khi bắt đầu workshop này, hãy đảm bảo bạn đã chuẩn bị sẵn những điều sau.

---

## 1. Tài khoản AWS

- Một **tài khoản AWS** đang hoạt động với billing được kích hoạt
- Khuyến nghị: Tạo IAM user riêng thay vì sử dụng root account
- **AWS Region**: Sử dụng `us-east-1` (N. Virginia) xuyên suốt workshop để đảm bảo nhất quán

> 💡 **Mẹo:** Nếu bạn đang sử dụng tài khoản AWS có credit khuyến mãi (ví dụ từ FCAJ), hãy kiểm tra số dư credit còn lại trước khi bắt đầu.

---

## 2. Quyền IAM Cần Thiết

IAM user hoặc role của bạn phải có quyền cho các dịch vụ sau. Để đơn giản trong workshop này, bạn có thể gán các policy AWS managed sau:

| AWS Managed Policy | Dịch vụ được bao phủ |
|-------------------|-----------------------|
| `AmazonS3FullAccess` | Tạo S3 bucket, đọc/ghi |
| `AWSGlueConsoleFullAccess` | Glue ETL jobs, Data Catalog |
| `AmazonAthenaFullAccess` | Thực thi truy vấn Athena |
| `AmazonEC2FullAccess` | EC2, VPC, Security Group, Elastic IP |
| `AWSLambda_FullAccess` | Tạo Lambda function |
| `AmazonAPIGatewayAdministrator` | Cấu hình API Gateway |
| `CloudWatchFullAccess` | Log, metric, alarm |
| `AWSKeyManagementServicePowerUser` | Tạo và sử dụng KMS key |
| `IAMFullAccess` | Tạo IAM role cho các dịch vụ |

> ⚠️ **Lưu ý:** Trong môi trường production, bạn nên áp dụng các policy quyền hạn tối thiểu thay vì full access. Những quyền trên chỉ để thuận tiện cho workshop.

---

## 3. Công cụ & Phần mềm

### AWS CLI v2

Cài đặt và cấu hình AWS CLI v2:

```bash
# Xác minh cài đặt
aws --version
# Kết quả mong đợi: aws-cli/2.x.x

# Cấu hình thông tin xác thực
aws configure
# Nhập: AWS Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Xác minh cấu hình hoạt động
aws sts get-caller-identity
# Kết quả mong đợi: Account ID và ARN IAM user/role của bạn
```

### Python 3.9+

```bash
python --version
# Kết quả mong đợi: Python 3.9.x hoặc cao hơn
```

### Các package Python cần thiết (để test local):

```bash
pip install boto3 pandas streamlit plotly awswrangler pyathena
```

### Git (tùy chọn, để quản lý source code):

```bash
git --version
```

---

## 4. File Dữ liệu Mẫu

Workshop này sử dụng dữ liệu thương mại điện tử tổng hợp. Bạn cần các file CSV sau để tải lên S3:

| File | Các cột | Mô tả |
|------|---------|-------|
| `customers.csv` | customer_id, name, email, country, signup_date | Dữ liệu khách hàng chính |
| `orders.csv` | order_id, customer_id, total_usd, payment_method, device, source, country, order_time | Giao dịch đơn hàng |
| `products.csv` | product_id, name, category, price_usd | Danh mục sản phẩm |
| `order_items.csv` | item_id, order_id, product_id, quantity, price_usd | Các dòng mặt hàng trong đơn hàng |
| `reviews.csv` | review_id, order_id, rating, comment, review_date | Đánh giá khách hàng |
| `sessions.csv` | session_id, customer_id, start_time, end_time, device, source | Dữ liệu phiên web/app |

Bạn có thể tạo dữ liệu tổng hợp bằng Python:

```python
import pandas as pd
import random
from datetime import datetime, timedelta

# Tạo đơn hàng mẫu (10.000 bản ghi)
orders = []
for i in range(10000):
    orders.append({
        'order_id': f'ORD-{i:05d}',
        'customer_id': f'CUST-{random.randint(1, 2000):04d}',
        'total_usd': round(random.uniform(10, 500), 2),
        'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'source': random.choice(['organic', 'social', 'email', 'paid_ads']),
        'country': random.choice(['US', 'UK', 'DE', 'FR', 'JP', 'VN', 'SG']),
        'order_time': (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))).isoformat()
    })

pd.DataFrame(orders).to_csv('orders.csv', index=False)
print("Đã tạo orders.csv với 10.000 bản ghi")
```

---

## 5. Ước tính Chi phí

| Dịch vụ | Mức sử dụng Workshop | Chi phí ước tính |
|---------|----------------------|------------------|
| EC2 t3.micro | 4–5 giờ | ~$0.05 |
| Lưu trữ S3 | ~500 MB tổng | ~$0.01 |
| Glue ETL (3 jobs) | 3 × 2 DPU × 5 phút | ~$0.15 |
| Truy vấn Athena | ~10 truy vấn × 50 MB | ~$0.00 |
| API Gateway | ~100 yêu cầu test | ~$0.00 |
| Data Firehose | ~1 MB dữ liệu test | ~$0.00 |
| CloudWatch | Metric mặc định | ~$0.00 |
| **Tổng cộng** | | **~$0.21–$0.50** |

> 💡 **FinOps tip:** Luôn dọn dẹp tài nguyên sau workshop (xem Phần 5.5) để tránh các khoản phí phát sinh.

---

## 6. Kiến thức Tiên quyết

Bạn nên có hiểu biết cơ bản về:

- **Điều hướng AWS Console** - tạo và xem tài nguyên
- **Kiến thức Python cơ bản** - đọc và hiểu code PySpark/Pandas
- **SQL cơ bản** - câu lệnh SELECT, GROUP BY, ORDER BY
- **Khái niệm Networking** - VPC, subnet và security group là gì
- **Kiến thức cơ bản về S3** - tạo bucket và tải file lên

Không cần kinh nghiệm trước với Glue, Athena, hoặc Streamlit - workshop này dạy từ đầu.

---

## Danh sách kiểm tra trước khi bắt đầu

Trước khi tiến hành Bước 1, hãy xác nhận tất cả các mục dưới đây:

-  Tài khoản AWS đang hoạt động với billing được kích hoạt
-  IAM user/role có các quyền cần thiết liệt kê ở trên
-  AWS CLI v2 đã cài đặt và cấu hình (`aws sts get-caller-identity` trả về Account ID của bạn)
-  Python 3.9+ đã cài đặt
-  File CSV dữ liệu mẫu đã sẵn sàng (hoặc được tạo bằng script ở trên)
-  AWS Region đã đặt thành `us-east-1`

✅ **Đã kiểm tra hết?** Tiến hành đến [Mô tả Kiến trúc](../5.3-Architecture/)
