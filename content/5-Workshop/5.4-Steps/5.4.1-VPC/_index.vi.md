---
title: "Bước 1: VPC & Networking"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

# Bước 1: Thiết lập VPC & Networking

Trong bước này, bạn sẽ tạo nền tảng mạng cho workshop: một VPC với public subnet, Internet Gateway, Route Table và Security Group để lưu trữ EC2 Streamlit dashboard.

**Thời gian ước tính:** 15–20 phút

---

## Điều kiện tiên quyết

- Tài khoản AWS với quyền `AmazonEC2FullAccess`
- AWS Region: `us-east-1`

---

## 1.1 Tạo VPC

**AWS Console → VPC → Your VPCs → Create VPC**

| Trường | Giá trị |
|--------|---------|
| Name tag | `lakehouse-vpc` |
| IPv4 CIDR block | `10.0.0.0/16` |
| IPv6 CIDR block | No IPv6 CIDR block |
| Tenancy | Default |

Click **Create VPC**.

**Tùy chọn CLI:**
```bash
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=lakehouse-vpc}]' \
    --query "Vpc.VpcId" \
    --output text
```

![VPC đã tạo - Danh sách Your VPCs hiển thị lakehouse-vpc](/result/VPC/Your%20VPCs..jpg)

---

## 1.2 Tạo Public Subnet

**VPC Console → Subnets → Create Subnet**

| Trường | Giá trị |
|--------|---------|
| VPC | Chọn `lakehouse-vpc` |
| Subnet name | `lakehouse-public-subnet` |
| Availability Zone | `us-east-1a` |
| IPv4 CIDR block | `10.0.1.0/24` |

Click **Create Subnet**.

Sau khi tạo, chọn subnet → **Actions → Edit subnet settings**:
- ✅ Bật **Auto-assign public IPv4 address**

Click **Save**.

**Tùy chọn CLI:**
```bash
# Lấy VPC ID trước
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].VpcId" --output text)

# Tạo subnet
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=lakehouse-public-subnet}]'
```

![Subnet đã tạo trong lakehouse-vpc](/result/VPC/Subnets.jpg)

---

## 1.3 Tạo và Gắn Internet Gateway

**VPC Console → Internet Gateways → Create Internet Gateway**

| Trường | Giá trị |
|--------|---------|
| Name tag | `lakehouse-igw` |

Click **Create Internet Gateway**.

Sau đó **Actions → Attach to VPC** → chọn `lakehouse-vpc` → **Attach internet gateway**.

**Tùy chọn CLI:**
```bash
# Tạo IGW
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=lakehouse-igw}]' \
    --query "InternetGateway.InternetGatewayId" --output text)

# Gắn vào VPC
aws ec2 attach-internet-gateway \
    --internet-gateway-id $IGW_ID \
    --vpc-id $VPC_ID
```

![Internet Gateway gắn vào lakehouse-vpc](/result/VPC/Internet%20Gateway.jpg)

---

## 1.4 Cấu hình Route Table

**VPC Console → Route Tables**

Chọn Route Table liên kết với `lakehouse-vpc` (hoặc tạo mới đặt tên `lakehouse-rt`).

**Tab Routes → Edit routes → Add route:**

| Đích đến | Mục tiêu |
|----------|----------|
| `0.0.0.0/0` | `lakehouse-igw` (Internet Gateway) |

Click **Save changes**.

**Tab Subnet associations → Edit subnet associations:**
- Chọn `lakehouse-public-subnet`

Click **Save associations**.

**Tùy chọn CLI:**
```bash
# Lấy Route Table ID (route table chính của VPC)
RT_ID=$(aws ec2 describe-route-tables \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \
    --query "RouteTables[0].RouteTableId" --output text)

# Thêm route internet
aws ec2 create-route \
    --route-table-id $RT_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Liên kết subnet
SUBNET_ID=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].SubnetId" --output text)

aws ec2 associate-route-table \
    --route-table-id $RT_ID \
    --subnet-id $SUBNET_ID
```

![Route Tables - Route 0.0.0.0/0 trỏ tới Internet Gateway](/result/VPC/Route%20Tables.jpg)

---

## 1.5 Tạo Security Group cho EC2

**VPC Console → Security Groups → Create Security Group**

| Trường | Giá trị |
|--------|---------|
| Security group name | `lakehouse-ec2-sg` |
| Description | `Allow SSH and Streamlit access` |
| VPC | `lakehouse-vpc` |

**Inbound rules - Thêm rules:**

| Loại | Protocol | Port | Nguồn | Mô tả |
|------|----------|------|-------|-------|
| SSH | TCP | 22 | `My IP` | Quản lý SSH |
| Custom TCP | TCP | 8501 | `0.0.0.0/0` | Streamlit dashboard |

**Outbound rules:** Giữ mặc định (cho phép tất cả traffic).

Click **Create security group**.

> ⚠️ **Lưu ý bảo mật:** Trong production, hãy giới hạn port 8501 cho dải IP của công ty thay vì `0.0.0.0/0`. Cho workshop này, cho phép tất cả IP là chấp nhận được cho môi trường test tạm thời.

**Tùy chọn CLI:**
```bash
SG_ID=$(aws ec2 create-security-group \
    --group-name lakehouse-ec2-sg \
    --description "Allow SSH and Streamlit access" \
    --vpc-id $VPC_ID \
    --query "GroupId" --output text)

# Thêm rule SSH (thay YOUR_IP)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr $(curl -s https://checkip.amazonaws.com)/32

# Thêm rule Streamlit
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8501 \
    --cidr 0.0.0.0/0
```

![Security Group - Inbound rules hiển thị port 22 và 8501](/result/VPC/Security%20Group.jpg)

---

## 1.6 Kiểm tra & Xác nhận

Xác minh cài đặt mạng của bạn:

```bash
# Xác minh VPC tồn tại và đang hoạt động
aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].{VpcId:VpcId,CIDR:CidrBlock,State:State}"

# Xác minh subnet
aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].{SubnetId:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,MapPublicIp:MapPublicIpOnLaunch}"

# Xác minh Internet Gateway đã gắn
aws ec2 describe-internet-gateways \
    --filters "Name=tag:Name,Values=lakehouse-igw" \
    --query "InternetGateways[0].{IGWId:InternetGatewayId,Attachments:Attachments}"
```

**Kết quả mong đợi:**
- VPC: `State: available`
- Subnet: `MapPublicIp: true`
- IGW: `Attachments[0].State: available`

---

## Xử lý sự cố

| Vấn đề | Nguyên nhân | Cách khắc phục |
|--------|-------------|----------------|
| Không SSH được vào EC2 (tạo ở Bước 5) | Security Group thiếu rule port 22 | Thêm inbound SSH rule từ IP của bạn |
| Streamlit không truy cập được trên port 8501 | Security Group thiếu port 8501 | Thêm inbound Custom TCP rule cho port 8501 |
| EC2 không có internet | Route Table thiếu route 0.0.0.0/0 → IGW | Thêm route và liên kết với subnet |
| EC2 chỉ có private IP | Auto-assign public IP bị tắt | Chỉnh sửa subnet settings → bật auto-assign |

✅ **Bước 1 hoàn thành** - Tiến hành đến [Bước 2: S3 Buckets & Data Upload](../5.4.2-S3/)
