---
title: "Dọn dẹp tài nguyên"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5.5 </b> "
---

# Dọn dẹp Tài nguyên

Sau khi hoàn thành workshop, điều **quan trọng** là phải xóa tất cả tài nguyên AWS để tránh các khoản phí phát sinh. Thực hiện theo danh sách kiểm tra theo thứ tự - một số tài nguyên phụ thuộc vào các tài nguyên khác phải được xóa trước.

> ⚠️ **Quan trọng:** Bỏ qua dọn dẹp sẽ dẫn đến các khoản phí phát sinh. EC2 instance, Elastic IP và Glue ETL job vẫn hoạt động sẽ tiếp tục tính phí tài khoản của bạn.

**Thời gian ước tính:** 15–20 phút

---

## Thứ tự Dọn dẹp

Tài nguyên phải được xóa theo thứ tự sau để tránh lỗi phụ thuộc:

```
1. EC2 Instance (terminate)
2. Elastic IP (release)
3. Glue ETL Jobs (xóa 3 jobs)
4. Glue Catalog Tables + Database (xóa 7 bảng, sau đó database)
5. S3 Bucket (làm trống trước, sau đó xóa)
6. CloudWatch Alarms + Dashboard + Log Groups
7. VPC + Subnet + IGW + Route Table + Security Group
8. IAM Roles (Glue role + EC2 role)
9. SNS Topic
10. Firehose Stream (nếu đã tạo)
```

---

## Bước 1: Dừng và Terminate EC2 Instance

> ⚠️ **Lưu ý:** Terminate sẽ xóa EBS volume và tất cả dữ liệu trên đó. Nếu muốn giữ code Streamlit app, SCP file về máy local trước:
> ```bash
> scp -i lakehouse-key.pem ec2-user@<elastic-ip>:~/app_beautiful.py ./app_beautiful.py
> ```

**AWS Console → EC2 → Instances → Chọn `lakehouse-dashboard`**
- **Instance state → Terminate instance** → Xác nhận

```bash
# Lấy Instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Terminate instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID

# Xác minh terminate (đợi ~30 giây)
aws ec2 describe-instances --instance-ids $INSTANCE_ID \
    --query "Reservations[0].Instances[0].State.Name"
# Kết quả mong đợi: "terminated"
```

---

## Bước 2: Release Elastic IP

> ⚠️ **Cảnh báo chi phí:** Elastic IP được phân bổ nhưng không liên kết với instance đang chạy bị tính phí **$0.005/giờ** (~$3.60/tháng). Giải phóng ngay sau khi terminate EC2 instance.

**AWS Console → EC2 → Elastic IPs → Chọn IP → Actions → Release Elastic IP address**

```bash
# Tìm Allocation ID
aws ec2 describe-addresses \
    --query "Addresses[*].{IP:PublicIp,AllocId:AllocationId}" \
    --output table

# Giải phóng (thay alloc-xxxxxxxxxx bằng ID thực tế)
aws ec2 release-address --allocation-id alloc-xxxxxxxxxx
```

---

## Bước 3: Xóa Glue ETL Jobs

**AWS Console → AWS Glue → ETL Jobs**

Chọn tất cả ba jobs → **Actions → Delete** → Xác nhận:
- `raw-to-bronze-job`
- `bronze-to-silver-job`
- `silver-to-gold-job`

```bash
aws glue delete-job --job-name raw-to-bronze-job
aws glue delete-job --job-name bronze-to-silver-job
aws glue delete-job --job-name silver-to-gold-job
echo "Tất cả Glue jobs đã xóa"
```

---

## Bước 4: Xóa Glue Catalog Tables và Database

**Xóa bảng trước (bắt buộc trước khi xóa database):**

```bash
# Xóa tất cả 7 bảng Gold
for table in event_summary daily_revenue payment_summary country_revenue device_summary source_summary dashboard_summary; do
    aws glue delete-table --database-name customer_behavior_catalog_db --name $table
    echo "Đã xóa bảng: $table"
done
```

**Sau đó xóa database:**

```bash
aws glue delete-database --name customer_behavior_catalog_db
echo "Đã xóa Glue database"
```

---

## Bước 5: Làm trống và Xóa S3 Bucket

S3 bucket không thể xóa trừ khi hoàn toàn trống (bao gồm tất cả versions nếu versioning được bật).

```bash
# Xóa tất cả objects hiện tại
aws s3 rm s3://customer-behavior-lakehouse1 --recursive
echo "Tất cả objects hiện tại đã xóa"

# Xóa tất cả versioned objects (nếu versioning được bật)
aws s3api delete-objects \
    --bucket customer-behavior-lakehouse1 \
    --delete "$(aws s3api list-object-versions \
        --bucket customer-behavior-lakehouse1 \
        --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}' \
        --output json)"

# Xóa tất cả delete markers
aws s3api delete-objects \
    --bucket customer-behavior-lakehouse1 \
    --delete "$(aws s3api list-object-versions \
        --bucket customer-behavior-lakehouse1 \
        --query '{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' \
        --output json)"

# Bây giờ xóa bucket
aws s3 rb s3://customer-behavior-lakehouse1 --force
echo "S3 bucket đã xóa"
```

> 📌 **Mẹo:** Nếu bucket có nhiều versioned objects, sử dụng S3 Console thay thế:
> S3 → Chọn bucket → **Empty** → gõ "permanently delete" → **Empty**
> Sau đó: **Delete** → gõ tên bucket → **Delete bucket**

---

## Bước 6: Xóa CloudWatch Alarms, Dashboard và Log Groups

```bash
# Xóa alarms
aws cloudwatch delete-alarms \
    --alarm-names "GlueJobFailure-Alert" "Athena-DataScan-Alert" "EC2-CPU-High-Alert"
echo "CloudWatch alarms đã xóa"

# Xóa CloudWatch dashboard
aws cloudwatch delete-dashboards --dashboard-names "lakehouse-pipeline-health"
echo "CloudWatch dashboard đã xóa"

# Xóa Glue job log groups
aws logs delete-log-group --log-group-name /aws-glue/jobs/output
aws logs delete-log-group --log-group-name /aws-glue/jobs/error

# Xóa Lambda log groups (nếu đã tạo)
aws logs delete-log-group --log-group-name /aws/lambda/firehose-transform 2>/dev/null || true
echo "Log groups đã xóa"
```

---

## Bước 7: Xóa VPC và Tài nguyên Networking

Xóa theo đúng thứ tự này (phụ thuộc phải được xóa trước):

```bash
# Lấy Resource IDs
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].VpcId" --output text)

IGW_ID=$(aws ec2 describe-internet-gateways \
    --filters "Name=tag:Name,Values=lakehouse-igw" \
    --query "InternetGateways[0].InternetGatewayId" --output text)

SUBNET_ID=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].SubnetId" --output text)

SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=lakehouse-ec2-sg" \
    --query "SecurityGroups[0].GroupId" --output text)

# 1. Xóa Security Group
aws ec2 delete-security-group --group-id $SG_ID
echo "Security Group đã xóa"

# 2. Tách và xóa Internet Gateway
aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID
echo "Internet Gateway đã xóa"

# 3. Xóa Subnet
aws ec2 delete-subnet --subnet-id $SUBNET_ID
echo "Subnet đã xóa"

# 4. Xóa VPC (phải là cuối cùng)
aws ec2 delete-vpc --vpc-id $VPC_ID
echo "VPC đã xóa"
```

---

## Bước 8: Xóa IAM Roles

```bash
# --- Xóa Glue ETL Role ---
# Tách managed policies
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess

# Xóa Glue role
aws iam delete-role --role-name AWSGlueServiceRole-lakehouse
echo "Glue IAM role đã xóa"

# --- Xóa EC2 Dashboard Role ---
aws iam detach-role-policy \
    --role-name lakehouse-ec2-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess
aws iam detach-role-policy \
    --role-name lakehouse-ec2-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Xóa EC2 role
aws iam delete-role --role-name lakehouse-ec2-role
echo "EC2 IAM role đã xóa"
```

---

## Bước 9: Xóa SNS Topic

```bash
# Tìm SNS topic ARN
SNS_ARN=$(aws sns list-topics \
    --query "Topics[?contains(TopicArn,'lakehouse')].TopicArn" \
    --output text)

# Xóa SNS topic (hủy đăng ký tất cả endpoints)
[ ! -z "$SNS_ARN" ] && aws sns delete-topic --topic-arn $SNS_ARN && echo "SNS topic đã xóa"
```

---

## Bước 10: Xóa Firehose Stream (Nếu đã tạo)

```bash
aws firehose delete-delivery-stream --delivery-stream-name lakehouse-event-stream 2>/dev/null && \
    echo "Firehose stream đã xóa" || echo "Firehose stream không tìm thấy (bỏ qua)"
```

---

## Kiểm tra Cuối cùng

Chạy kiểm tra toàn diện này để tìm bất kỳ tài nguyên billable nào còn lại:

```bash
echo "========================================="
echo "=== Kiểm tra tài nguyên còn lại ==="
echo "========================================="

echo ""
echo "--- EC2 Instances đang chạy/dừng ---"
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running,stopped" \
    --query "Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[?Key=='Name'].Value|[0]}" \
    --output table

echo ""
echo "--- Elastic IPs đã phân bổ ---"
aws ec2 describe-addresses \
    --query "Addresses[*].{IP:PublicIp,AllocId:AllocationId,AssocId:AssociationId}" \
    --output table

echo ""
echo "--- S3 Buckets (lakehouse) ---"
aws s3 ls | grep lakehouse

echo ""
echo "--- Glue Jobs ---"
aws glue list-jobs --query "JobNames" --output text | tr '\t' '\n' | grep lakehouse

echo ""
echo "--- Glue Databases ---"
aws glue get-databases --query "DatabaseList[?contains(Name,'customer')].Name" --output text

echo ""
echo "--- CloudWatch Alarms ---"
aws cloudwatch describe-alarms \
    --query "MetricAlarms[?contains(AlarmName,'lakehouse')||contains(AlarmName,'Glue')||contains(AlarmName,'Athena')||contains(AlarmName,'EC2')].{Name:AlarmName,State:StateValue}" \
    --output table

echo ""
echo "--- SNS Topics ---"
aws sns list-topics --query "Topics[?contains(TopicArn,'lakehouse')].TopicArn" --output text

echo "========================================="
echo "Kết quả mong đợi: Tất cả phần trên đều trống (không có tài nguyên còn lại)"
echo "========================================="
```

**Kết quả mong đợi:** Tất cả phần đều trống (không có tài nguyên còn lại).

---

## Danh sách Kiểm tra Dọn dẹp

Hoàn thành danh sách kiểm tra này để xác nhận mọi thứ đã xóa:

-  EC2 instance `lakehouse-dashboard` đã terminate
-  Elastic IP đã giải phóng
-  `raw-to-bronze-job` đã xóa
-  `bronze-to-silver-job` đã xóa
-  `silver-to-gold-job` đã xóa
-  7 bảng Glue Catalog đã xóa
-  Database Glue `customer_behavior_catalog_db` đã xóa
-  S3 bucket `customer-behavior-lakehouse1` đã làm trống và xóa
-  CloudWatch alarm `GlueJobFailure-Alert` đã xóa
-  CloudWatch alarm `Athena-DataScan-Alert` đã xóa
-  CloudWatch alarm `EC2-CPU-High-Alert` đã xóa
-  CloudWatch dashboard `lakehouse-pipeline-health` đã xóa
-  CloudWatch log groups đã xóa
-  Security Group `lakehouse-ec2-sg` đã xóa
-  Internet Gateway `lakehouse-igw` đã xóa
-  Subnet `lakehouse-public-subnet` đã xóa
-  VPC `lakehouse-vpc` đã xóa
-  IAM role `AWSGlueServiceRole-lakehouse` đã xóa
-  IAM role `lakehouse-ec2-role` đã xóa
-  SNS topic `lakehouse-alerts` đã xóa
-  Firehose stream `lakehouse-event-stream` đã xóa (nếu đã tạo)

✅ **Workshop hoàn thành!** Tất cả tài nguyên đã được dọn dẹp. Không có thêm khoản phí nào phát sinh.

---

## Chúc mừng!

Hoàn thành thành công workshop **FinOps-Optimized Serverless Medallion Data Lakehouse**. Xây dựng một data analytics pipeline end-to-end hoàn chỉnh trên AWS:

- ✅ Tiếp nhận streaming events (Firehose) và dữ liệu CSV batch (Lambda)
- ✅ Xử lý dữ liệu qua 4 tầng Medallion: Raw → Bronze → Silver → Gold
- ✅ Truy vấn KPI nghiệp vụ serverless với Amazon Athena
- ✅ Trực quan hóa insights trong Streamlit dashboard trên EC2
- ✅ Giám sát pipeline với CloudWatch alarms
- ✅ Giữ chi phí tối thiểu với FinOps best practices (Parquet, serverless, pay-per-use)
