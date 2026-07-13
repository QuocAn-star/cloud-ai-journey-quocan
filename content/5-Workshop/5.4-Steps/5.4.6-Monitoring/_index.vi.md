---
title: "Bước 6: Giám sát"
date: 2024-01-01
weight: 6
chapter: false
pre: " <b> 5.4.6 </b> "
---

# Bước 6: Giám sát với CloudWatch

Trong bước này, bạn sẽ thiết lập giám sát và cảnh báo cho toàn bộ data pipeline sử dụng Amazon CloudWatch - bao gồm tình trạng Glue ETL job, metric truy vấn Athena và tình trạng EC2 instance.

**Thời gian ước tính:** 20–25 phút

---

## Điều kiện tiên quyết

- Các Bước 3–5 hoàn thành (Glue jobs, Athena và EC2 dashboard đều đang chạy)
- Quyền IAM `CloudWatchFullAccess`

---

## 6.1 Xem Log Glue ETL Job

Mỗi lần chạy Glue ETL job tự động tạo log trong CloudWatch Logs.

**AWS Console → AWS Glue → ETL Jobs → [tên job] → Tab Runs**

Click bất kỳ run → Link **View CloudWatch logs**.

Hoặc điều hướng trực tiếp:
**CloudWatch Console → Log groups → `/aws-glue/jobs/output`**

**Xem log qua CLI:**
```bash
# Lấy chi tiết log group cho một run cụ thể
aws glue get-job-runs --job-name silver-to-gold-job \
    --query "JobRuns[0].{Status:JobRunState,LogGroup:LogGroupName,Duration:ExecutionTime}"

# Theo dõi output logs (live follow)
aws logs tail /aws-glue/jobs/output --follow

# Lấy 20 events gần nhất từ error log group
aws logs tail /aws-glue/jobs/error --follow
```

**Các thông điệp log chính để xác minh thành công:**

```
Reading Silver: s3://customer-behavior-lakehouse1/silver/events/
Writing Gold: s3://customer-behavior-lakehouse1/gold/event_summary/
Registered Glue Catalog table: event_summary
Registered Glue Catalog table: daily_revenue
...
Silver to Gold job completed and Glue Catalog tables registered.
```

---

## 6.2 Thiết lập CloudWatch Alarm cho Glue Jobs

**AWS Console → CloudWatch → Alarms → Create alarm**

### Alarm 1: Cảnh báo Glue Job Thất bại

| Trường | Giá trị |
|--------|---------|
| Metric namespace | Glue |
| Metric name | `glue.driver.aggregate.numFailedTasks` |
| Statistic | Sum |
| Period | 5 phút |
| Threshold type | Static |
| Condition | `> 0` |
| Alarm name | `GlueJobFailure-Alert` |
| Notification | Tạo SNS topic → nhập email của bạn |

Click **Create alarm**.

**Tùy chọn CLI:**
```bash
# Bước 1: Tạo SNS topic cho cảnh báo
SNS_ARN=$(aws sns create-topic --name lakehouse-alerts --query "TopicArn" --output text)
echo "SNS ARN: $SNS_ARN"

# Bước 2: Đăng ký email của bạn (kiểm tra hộp thư để xác nhận)
aws sns subscribe \
    --topic-arn $SNS_ARN \
    --protocol email \
    --notification-endpoint your-email@example.com

# Bước 3: Tạo alarm thất bại Glue
aws cloudwatch put-metric-alarm \
    --alarm-name "GlueJobFailure-Alert" \
    --alarm-description "Cảnh báo khi Glue ETL job có task thất bại" \
    --metric-name "glue.driver.aggregate.numFailedTasks" \
    --namespace "Glue" \
    --statistic Sum \
    --period 300 \
    --threshold 0 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions $SNS_ARN
```

---

## 6.3 Thiết lập CloudWatch Alarm cho Athena

### Alarm 2: Cảnh báo Chi phí Quét Dữ liệu Athena

Theo dõi tổng dữ liệu được quét mỗi ngày - cảnh báo khi tiệm cận giới hạn chi phí.

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "Athena-DataScan-Alert" \
    --alarm-description "Cảnh báo khi Athena quét hơn 5 GB trong một ngày" \
    --metric-name "DataScannedInBytes" \
    --namespace "AWS/Athena" \
    --dimensions Name=WorkGroup,Value=lakehouse-wg \
    --statistic Sum \
    --period 86400 \
    --threshold 5368709120 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions $SNS_ARN
```

> 💡 **FinOps note:** Ngưỡng 5 GB = trigger cảnh báo $0.025. Với hiệu quả Parquet, ngưỡng này hiếm khi bị vượt trong quá trình sử dụng bình thường.

---

## 6.4 Giám sát Tình trạng EC2 Instance

### Alarm 3: Cảnh báo CPU EC2 Cao

**CloudWatch Console → All metrics → EC2 → Per-Instance Metrics**

Chọn instance `lakehouse-dashboard` và xem:
- **CPUUtilization** - nên thấp (~5–20%) khi nhàn rỗi
- **NetworkIn/NetworkOut** - traffic từ người dùng truy cập dashboard

```bash
# Lấy EC2 Instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Tạo alarm CPU cao
aws cloudwatch put-metric-alarm \
    --alarm-name "EC2-CPU-High-Alert" \
    --alarm-description "EC2 CPU trên 80% trong 5 phút liên tiếp" \
    --metric-name "CPUUtilization" \
    --namespace "AWS/EC2" \
    --dimensions Name=InstanceId,Value=$INSTANCE_ID \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions $SNS_ARN
```

---

## 6.5 Tạo CloudWatch Dashboard

Tạo dashboard thống nhất để xem tất cả metric tình trạng pipeline ở một nơi.

**CloudWatch Console → Dashboards → Create dashboard**

| Trường | Giá trị |
|--------|---------|
| Dashboard name | `lakehouse-pipeline-health` |

**Thêm widgets:**

| Widget | Metric | Loại biểu đồ |
|--------|--------|-----------| 
| Glue Completed Tasks | `Glue / glue.driver.aggregate.numCompletedTasks` | Line |
| Glue Failed Tasks | `Glue / glue.driver.aggregate.numFailedTasks` | Line |
| Athena Data Scanned | `AWS/Athena / DataScannedInBytes` (Workgroup=lakehouse-wg) | Bar |
| EC2 CPU Utilization | `AWS/EC2 / CPUUtilization` (InstanceId=của bạn) | Line |

**CLI để tạo dashboard:**
```bash
aws cloudwatch put-dashboard \
    --dashboard-name "lakehouse-pipeline-health" \
    --dashboard-body '{
        "widgets": [
            {
                "type": "metric",
                "x": 0, "y": 0, "width": 12, "height": 6,
                "properties": {
                    "title": "EC2 CPU Utilization (%)",
                    "metrics": [["AWS/EC2","CPUUtilization","InstanceId","'"$INSTANCE_ID"'"]],
                    "period": 300,
                    "stat": "Average",
                    "view": "timeSeries"
                }
            },
            {
                "type": "metric",
                "x": 12, "y": 0, "width": 12, "height": 6,
                "properties": {
                    "title": "Athena Data Scanned (Bytes)",
                    "metrics": [["AWS/Athena","DataScannedInBytes","WorkGroup","lakehouse-wg"]],
                    "period": 86400,
                    "stat": "Sum",
                    "view": "bar"
                }
            },
            {
                "type": "metric",
                "x": 0, "y": 6, "width": 12, "height": 6,
                "properties": {
                    "title": "Glue Job - Completed Tasks",
                    "metrics": [["Glue","glue.driver.aggregate.numCompletedTasks"]],
                    "period": 300,
                    "stat": "Sum",
                    "view": "timeSeries"
                }
            },
            {
                "type": "metric",
                "x": 12, "y": 6, "width": 12, "height": 6,
                "properties": {
                    "title": "Glue Job - Failed Tasks",
                    "metrics": [["Glue","glue.driver.aggregate.numFailedTasks"]],
                    "period": 300,
                    "stat": "Sum",
                    "view": "timeSeries"
                }
            }
        ]
    }'
```

---

## 6.6 Xem Lambda Logs (Đường Tiếp nhận)

Nếu bạn đã cấu hình Lambda cho chuyển đổi Firehose hoặc trích xuất DB batch:

**CloudWatch Console → Log groups → `/aws/lambda/<tên-function>`**

```bash
# Liệt kê log streams
aws logs describe-log-streams \
    --log-group-name /aws/lambda/firehose-transform \
    --order-by LastEventTime \
    --descending \
    --query "logStreams[0].logStreamName" \
    --output text

# Lấy log events gần nhất
LOG_STREAM=$(aws logs describe-log-streams \
    --log-group-name /aws/lambda/firehose-transform \
    --order-by LastEventTime --descending \
    --query "logStreams[0].logStreamName" --output text)

aws logs get-log-events \
    --log-group-name /aws/lambda/firehose-transform \
    --log-stream-name "$LOG_STREAM" \
    --limit 20 \
    --query "events[*].message" \
    --output text
```

---

## 6.7 Tóm tắt: Các Alarm đã Cấu hình

| Tên Alarm | Metric | Ngưỡng | Hành động |
|-----------|--------|--------|-----------|
| `GlueJobFailure-Alert` | `numFailedTasks` | > 0 | Email SNS |
| `Athena-DataScan-Alert` | `DataScannedInBytes` | > 5 GB/ngày | Email SNS |
| `EC2-CPU-High-Alert` | `CPUUtilization` | > 80% trong 5 phút | Email SNS |

---

## 6.8 Kiểm tra Cảnh báo

Kích hoạt alarm test để xác minh thông báo SNS hoạt động:

```bash
# Ép alarm vào trạng thái ALARM (chỉ để test)
aws cloudwatch set-alarm-state \
    --alarm-name "GlueJobFailure-Alert" \
    --state-value ALARM \
    --state-reason "Kích hoạt test thủ công từ workshop"

# Kiểm tra hộp thư email để nhận thông báo SNS (đến trong ~1 phút)

# Đặt lại về OK sau khi test
aws cloudwatch set-alarm-state \
    --alarm-name "GlueJobFailure-Alert" \
    --state-value OK \
    --state-reason "Test hoàn thành - đặt lại alarm"
```

---

## 6.9 Kiểm tra Trạng thái Tất cả Alarm

```bash
# Xem tất cả lakehouse alarms và trạng thái hiện tại
aws cloudwatch describe-alarms \
    --alarm-names "GlueJobFailure-Alert" "Athena-DataScan-Alert" "EC2-CPU-High-Alert" \
    --query "MetricAlarms[*].{Name:AlarmName,State:StateValue,Reason:StateReason}" \
    --output table
```

**Trạng thái mong đợi:** Tất cả alarm nên hiển thị trạng thái `OK` trong quá trình pipeline hoạt động bình thường.

---

## Xử lý sự cố

| Vấn đề | Nguyên nhân | Cách khắc phục |
|--------|-------------|----------------|
| Không nhận được email SNS | Chưa xác nhận subscription | Kiểm tra hộp thư để tìm email xác nhận AWS và click link |
| Alarm ở trạng thái `INSUFFICIENT_DATA` | Chưa có dữ liệu metric | Chạy một Glue job hoặc Athena query để tạo metric |
| Log Glue không xuất hiện | Log group chưa được tạo | Chạy ít nhất một Glue job - log xuất hiện sau lần chạy đầu |
| Dashboard widgets hiển thị "No data" | Dimension metric không khớp | Xác minh Instance ID và tên workgroup trong widget config |

✅ **Bước 6 hoàn thành** - Pipeline của bạn được giám sát đầy đủ! Tiến hành đến [Dọn dẹp](../../5.5-Cleanup/) khi bạn đã hoàn thành khám phá.
