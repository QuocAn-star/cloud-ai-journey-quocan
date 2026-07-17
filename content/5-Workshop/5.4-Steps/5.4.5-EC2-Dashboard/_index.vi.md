---
title: "Bước 5: EC2 & Dashboard"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5.4.5 </b> "
---

# Bước 5: Deploy Streamlit Dashboard trên EC2

Trong bước này, bạn sẽ khởi chạy EC2 instance trong VPC, cài đặt Python dependencies, deploy ứng dụng Streamlit `app_beautiful.py` và truy cập dashboard phân tích trực tuyến.

**Thời gian ước tính:** 25–35 phút

---

## Điều kiện tiên quyết

- Bước 1 hoàn thành (VPC, subnet, security group `lakehouse-ec2-sg` đã tạo)
- Bước 4 hoàn thành (Athena có thể truy vấn các bảng Gold)
- File source `app_beautiful.py` đã sẵn sàng

---

## 5.1 Tạo IAM Role cho EC2

EC2 instance cần quyền để truy vấn Athena và đọc kết quả S3.

**AWS Console → IAM → Roles → Create role**

| Trường | Giá trị |
|--------|---------|
| Trusted entity type | AWS service |
| Service | EC2 |

**Thêm permissions:**
- `AmazonAthenaFullAccess` - để thực thi truy vấn
- `AmazonS3ReadOnlyAccess` - để đọc Gold và athena-results

**Tên role:** `lakehouse-ec2-role`

> ⚠️ **Lưu ý quyền hạn tối thiểu:** Trong production, thay các policy broad bằng custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryResults",
        "athena:GetQueryExecution",
        "athena:StopQueryExecution",
        "athena:GetWorkGroup"
      ],
      "Resource": "arn:aws:athena:us-east-1:*:workgroup/lakehouse-wg"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket", "s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/gold/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/athena-results/*",
        "arn:aws:s3:::customer-behavior-lakehouse1"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetTable", "glue:GetTables",
        "glue:GetDatabase", "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 5.2 Khởi chạy EC2 Instance

**AWS Console → EC2 → Instances → Launch instances**

| Trường | Giá trị |
|--------|---------|
| Name | `lakehouse-dashboard` |
| AMI | Amazon Linux 2023 AMI (đủ điều kiện free tier) |
| Instance type | `t3.micro` (đủ điều kiện Free Tier) |
| Key pair | Tạo mới: `lakehouse-key` → Tải file `.pem` về |
| VPC | `lakehouse-vpc` |
| Subnet | `lakehouse-public-subnet` |
| Auto-assign public IP | Bật |
| Security group | Chọn hiện có: `lakehouse-ec2-sg` |
| IAM instance profile | `lakehouse-ec2-role` |
| Storage | 8 GiB gp3 (EBS mặc định) |

Click **Launch instance**.

> ⚠️ **Cảnh báo key pair:** Tải và lưu file `.pem` ngay lập tức. Bạn không thể lấy lại sau khi tạo. Không có file này, bạn không thể SSH vào instance.

![EC2 Instance - lakehouse-dashboard đang chạy](/result/EC2/EC2%20Instance.jpg)

![EC2 Security Group - hiển thị inbound rules cho port 22 và 8501](/result/EC2/Security%20Group.jpg)

---

## 5.3 Gán Elastic IP (Khuyến nghị)

Elastic IP đảm bảo URL dashboard không thay đổi nếu EC2 instance được dừng và khởi động lại.

**AWS Console → EC2 → Elastic IPs → Allocate Elastic IP address**

- Click **Allocate** (cài đặt mặc định)

Sau đó **Actions → Associate Elastic IP address**:
- Instance: chọn `lakehouse-dashboard`
- Click **Associate**

Ghi lại địa chỉ Elastic IP - đây sẽ là URL dashboard của bạn: `http://<elastic-ip>:8501`

**Tùy chọn CLI:**
```bash
# Phân bổ Elastic IP
ALLOC_ID=$(aws ec2 allocate-address \
    --domain vpc \
    --query "AllocationId" --output text)

# Lấy Instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Liên kết
aws ec2 associate-address \
    --instance-id $INSTANCE_ID \
    --allocation-id $ALLOC_ID
```

---

## 5.4 Kết nối vào EC2 và Cài đặt Dependencies

SSH vào instance từ máy local của bạn:

```bash
# Đặt quyền đúng cho file key (Linux/Mac)
chmod 400 lakehouse-key.pem

# SSH vào EC2 (thay <elastic-ip> bằng IP thực tế của bạn)
ssh -i lakehouse-key.pem ec2-user@<elastic-ip>
```

Sau khi kết nối, cài đặt Python dependencies:

```bash
# Cập nhật packages hệ thống
sudo dnf update -y

# Cài đặt Python pip
sudo dnf install python3-pip -y

# Cài đặt tất cả Python packages cần thiết
pip3 install boto3 pandas streamlit plotly awswrangler pyathena

# Xác minh các package chính đã cài đúng
python3 -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python3 -c "import awswrangler; print('AWS Wrangler:', awswrangler.__version__)"
python3 -c "import plotly; print('Plotly:', plotly.__version__)"
```

---

## 5.5 Deploy Ứng dụng Streamlit

**Phương án A: Chuyển file qua SCP (từ máy local, terminal thứ 2)**

```bash
scp -i lakehouse-key.pem app_beautiful.py ec2-user@<elastic-ip>:~/app_beautiful.py
```

**Phương án B: Copy-paste trực tiếp trên EC2**

```bash
# Trên EC2: tạo file và paste nội dung
nano ~/app_beautiful.py
# Paste toàn bộ nội dung app_beautiful.py, sau đó Ctrl+X, Y, Enter
```

**Xác minh cấu hình trong `app_beautiful.py`:**

App chứa các biến cấu hình này - xác nhận chúng khớp với thiết lập của bạn:

```python
DATABASE = "customer_behavior_catalog_db"         # Glue database của bạn
ATHENA_OUTPUT = "s3://customer-behavior-lakehouse1/athena-results/"  # Path results của bạn
REGION = "us-east-1"                             # AWS region của bạn
```

Nếu bạn dùng tên bucket hoặc database khác ở các bước trước, hãy cập nhật các giá trị này.

---

## 5.6 Chạy Dashboard

```bash
# Khởi động Streamlit ở background (tiếp tục sau khi đóng SSH)
nohup streamlit run app_beautiful.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    > ~/streamlit.log 2>&1 &

# Đợi 3 giây để khởi động
sleep 3

# Kiểm tra logs khởi động
cat ~/streamlit.log
# Kết quả mong đợi:
# You can now view your Streamlit app in your browser.
# Local URL: http://0.0.0.0:8501

# Xác minh port 8501 đang lắng nghe
ss -tlnp | grep 8501
```

**Truy cập dashboard:**

Mở trình duyệt và điều hướng đến:
```
http://<elastic-ip>:8501
```

---

## 5.7 Các Phần Dashboard & Xác nhận

Ứng dụng Streamlit hiển thị các phần sau:

**KPI Cards (Đầu dashboard):**
- Tổng đơn hàng, Tổng khách hàng, Tổng doanh thu ($), Giá trị đơn TB, Tổng sự kiện

**Biểu đồ tương tác:**

![Xu hướng Doanh thu - biểu đồ vùng doanh thu hàng ngày theo thời gian](/result/DashBoard/Revenue%20Trend.png)

![Top 10 Quốc gia theo Doanh thu - biểu đồ cột ngang](/result/DashBoard/Top%2010%20Countries%20by%20Revenue.png)

![Doanh thu theo Loại Thiết bị - biểu đồ donut: mobile, desktop, tablet](/result/DashBoard/Revenue%20by%20Device.png)

![Doanh thu theo Phương thức Thanh toán - biểu đồ cột](/result/DashBoard/Revenue%20by%20Payment%20Method.png)

![Doanh thu theo Nguồn Traffic - biểu đồ cột](/result/DashBoard/Revenue%20by%20Traffic%20Source.png)

![Phân phối Sự kiện - biểu đồ cột theo loại sự kiện](/result/DashBoard/Event%20Distribution.png)

![Top Performers - bảng so sánh 3 cột](/result/DashBoard/Top%20Performers.jpg)

![Xem Dữ liệu Doanh thu Hàng ngày - bảng dữ liệu có thể mở rộng](/result/DashBoard/View%20Daily%20Revenue%20Data.jpg)

---

**Danh sách kiểm tra xác nhận:**

| Phần Dashboard | Nội dung mong đợi | Xác nhận |
|----------------|-------------------|----------|
| **KPI Cards** | 5 chỉ số, tất cả số > 0 | Xác minh giá trị khác 0 |
| **Revenue Trend** | Biểu đồ vùng với ngày trên trục x | Ngày hiển thị, doanh thu bằng $ |
| **Event Distribution** | Ít nhất 3–5 loại sự kiện | Cột hiển thị đúng |
| **Top 10 Countries** | Quốc gia sắp xếp theo doanh thu | Thứ tự giảm dần đúng |
| **Revenue by Device** | Donut với 3 phần | mobile, desktop, tablet |
| **Revenue by Payment** | Cột với các bars | credit_card, paypal, wallet, cod |
| **Revenue by Source** | Cột với các bars | organic, social, email, paid_ad,... |
| **Top Performers** | Bảng 3 cột | Top Countries, Top Devices, Top Sources |
| **Daily Revenue Data** | Bảng có thể mở rộng | Dữ liệu đầy đủ sắp theo ngày |

---

## 5.8 Giữ Dashboard Chạy Liên tục

Để đảm bảo dashboard tiếp tục chạy sau khi đóng phiên SSH, dùng systemd service:

```bash
# Tạo file systemd service
sudo tee /etc/systemd/system/streamlit.service << EOF
[Unit]
Description=Streamlit Lakehouse Dashboard
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user
ExecStart=/usr/local/bin/streamlit run /home/ec2-user/app_beautiful.py \
    --server.port 8501 \
    --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Bật và khởi động service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Kiểm tra trạng thái
sudo systemctl status streamlit
```

**Các lệnh quản lý hữu ích:**

```bash
# Xem logs dashboard trực tiếp
tail -f ~/streamlit.log

# Kiểm tra process đang chạy
ps aux | grep streamlit

# Dừng dashboard
pkill -f streamlit
# hoặc
sudo systemctl stop streamlit

# Khởi động lại sau khi cập nhật code
sudo systemctl restart streamlit
```

---

## Xử lý sự cố

| Vấn đề | Nguyên nhân | Cách khắc phục |
|--------|-------------|----------------|
| `Connection refused` trên port 8501 | Streamlit chưa khởi động hoặc bị crash | Kiểm tra `cat ~/streamlit.log` để xem lỗi |
| `Browser can't connect` | Security Group thiếu rule port 8501 | Thêm inbound Custom TCP rule cho 8501 |
| `AccessDeniedException` trong dashboard | EC2 IAM role thiếu quyền Athena/S3 | Kiểm tra `lakehouse-ec2-role` có đúng policies |
| `No module named 'awswrangler'` | Package chưa cài | Chạy `pip3 install awswrangler` trên EC2 |
| Dashboard hiển thị 0 cho tất cả metrics | Bảng Athena trống | Chạy lại silver-to-gold-job (Bước 3) |
| SSH connection refused | EC2 không chạy hoặc SG thiếu port 22 | Kiểm tra trạng thái EC2 trong Console, xác minh SG rules |


---

## Dashboard Trực tuyến

Dashboard của workshop đã được deploy và có thể truy cập tại link bên dưới. Bạn có thể khám phá tất cả biểu đồ tương tác và KPI metrics từ kết quả pipeline thực tế:

> 🔗 **[http://3.217.165.2:8502/](http://3.217.165.2:8502/)**


✅ **Bước 5 hoàn thành** - Tiến hành đến [Bước 6: Giám sát với CloudWatch](../5.4.6-Monitoring/)
