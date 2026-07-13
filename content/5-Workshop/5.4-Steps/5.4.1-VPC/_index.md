---
title: "Step 1: VPC & Networking"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

# Step 1: VPC & Networking Setup

In this step, you will create the network foundation for the workshop: a VPC with a public subnet, Internet Gateway, Route Table, and Security Group to host the EC2 Streamlit dashboard.

**Estimated time:** 15–20 minutes

---

## Prerequisites

- AWS account with `AmazonEC2FullAccess` permission
- AWS Region: `us-east-1`

---

## 1.1 Create a VPC

**AWS Console → VPC → Your VPCs → Create VPC**

| Field | Value |
|-------|-------|
| Name tag | `lakehouse-vpc` |
| IPv4 CIDR block | `10.0.0.0/16` |
| IPv6 CIDR block | No IPv6 CIDR block |
| Tenancy | Default |

Click **Create VPC**.

**CLI alternative:**
```bash
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=lakehouse-vpc}]' \
    --query "Vpc.VpcId" \
    --output text
```

![VPC created - Your VPCs list showing lakehouse-vpc](/result/VPC/Your%20VPCs..jpg)

---

## 1.2 Create a Public Subnet

**VPC Console → Subnets → Create Subnet**

| Field | Value |
|-------|-------|
| VPC | Select `lakehouse-vpc` |
| Subnet name | `lakehouse-public-subnet` |
| Availability Zone | `us-east-1a` |
| IPv4 CIDR block | `10.0.1.0/24` |

Click **Create Subnet**.

After creating, select the subnet → **Actions → Edit subnet settings**:
- ✅ Enable **Auto-assign public IPv4 address**

Click **Save**.

**CLI alternative:**
```bash
# Get VPC ID first
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].VpcId" --output text)

# Create subnet
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=lakehouse-public-subnet}]'
```

![Subnet created inside lakehouse-vpc](/result/VPC/Subnets.jpg)

---

## 1.3 Create and Attach an Internet Gateway

**VPC Console → Internet Gateways → Create Internet Gateway**

| Field | Value |
|-------|-------|
| Name tag | `lakehouse-igw` |

Click **Create Internet Gateway**.

Then **Actions → Attach to VPC** → select `lakehouse-vpc` → **Attach internet gateway**.

**CLI alternative:**
```bash
# Create IGW
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=lakehouse-igw}]' \
    --query "InternetGateway.InternetGatewayId" --output text)

# Attach to VPC
aws ec2 attach-internet-gateway \
    --internet-gateway-id $IGW_ID \
    --vpc-id $VPC_ID
```

![Internet Gateway attached to lakehouse-vpc](/result/VPC/Internet%20Gateway.jpg)

---

## 1.4 Configure Route Table

**VPC Console → Route Tables**

Select the Route Table associated with `lakehouse-vpc` (or create a new one named `lakehouse-rt`).

**Routes tab → Edit routes → Add route:**

| Destination | Target |
|-------------|--------|
| `0.0.0.0/0` | `lakehouse-igw` (Internet Gateway) |

Click **Save changes**.

**Subnet associations tab → Edit subnet associations:**
- Select `lakehouse-public-subnet`

Click **Save associations**.

**CLI alternative:**
```bash
# Get Route Table ID (main route table of VPC)
RT_ID=$(aws ec2 describe-route-tables \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \
    --query "RouteTables[0].RouteTableId" --output text)

# Add internet route
aws ec2 create-route \
    --route-table-id $RT_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associate subnet
SUBNET_ID=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].SubnetId" --output text)

aws ec2 associate-route-table \
    --route-table-id $RT_ID \
    --subnet-id $SUBNET_ID
```

![Route Tables - 0.0.0.0/0 route pointing to Internet Gateway](/result/VPC/Route%20Tables.jpg)

---

## 1.5 Create a Security Group for EC2

**VPC Console → Security Groups → Create Security Group**

| Field | Value |
|-------|-------|
| Security group name | `lakehouse-ec2-sg` |
| Description | `Allow SSH and Streamlit access` |
| VPC | `lakehouse-vpc` |

**Inbound rules - Add rules:**

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | `My IP` | SSH management access |
| Custom TCP | TCP | 8501 | `0.0.0.0/0` | Streamlit dashboard |

**Outbound rules:** Leave default (all traffic allowed).

Click **Create security group**.

> ⚠️ **Security note:** In production, restrict port 8501 to your company's IP range rather than `0.0.0.0/0`. For this workshop, allowing all IPs is acceptable for a temporary test environment.

**CLI alternative:**
```bash
SG_ID=$(aws ec2 create-security-group \
    --group-name lakehouse-ec2-sg \
    --description "Allow SSH and Streamlit access" \
    --vpc-id $VPC_ID \
    --query "GroupId" --output text)

# Add SSH rule (replace YOUR_IP)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr $(curl -s https://checkip.amazonaws.com)/32

# Add Streamlit rule
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8501 \
    --cidr 0.0.0.0/0
```

![Security Group - inbound rules showing port 22 and 8501](/result/VPC/Security%20Group.jpg)

---

## 1.6 Validation

Verify your networking setup:

```bash
# Verify VPC exists and is available
aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].{VpcId:VpcId,CIDR:CidrBlock,State:State}"

# Verify subnet
aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].{SubnetId:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,MapPublicIp:MapPublicIpOnLaunch}"

# Verify Internet Gateway is attached
aws ec2 describe-internet-gateways \
    --filters "Name=tag:Name,Values=lakehouse-igw" \
    --query "InternetGateways[0].{IGWId:InternetGatewayId,Attachments:Attachments}"
```

**Expected outputs:**
- VPC: `State: available`
- Subnet: `MapPublicIp: true`
- IGW: `Attachments[0].State: available`

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Cannot SSH to EC2 (created in Step 5) | Security Group missing port 22 rule | Add inbound SSH rule from your IP |
| Streamlit not accessible on port 8501 | Security Group missing port 8501 | Add inbound Custom TCP rule for port 8501 |
| EC2 has no internet access | Route Table missing 0.0.0.0/0 → IGW route | Add route and associate with subnet |
| EC2 has private IP only | Auto-assign public IP disabled | Edit subnet settings → enable auto-assign |

✅ **Step 1 complete** - Proceed to [Step 2: S3 Buckets & Data Upload](../5.4.2-S3/)
