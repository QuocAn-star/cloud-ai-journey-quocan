---
title: "Step 6: Monitoring"
date: 2024-01-01
weight: 6
chapter: false
pre: " <b> 5.4.6 </b> "
---

# Step 6: Monitoring with CloudWatch

In this step, you will set up monitoring and alerting for the entire data pipeline using Amazon CloudWatch - covering Glue ETL job health, Athena query metrics, and EC2 instance health.

**Estimated time:** 20–25 minutes

---

## Prerequisites

- Steps 3–5 complete (Glue jobs, Athena, and EC2 dashboard all running)
- `CloudWatchFullAccess` IAM permission

---

## 6.1 View Glue ETL Job Logs

Every Glue ETL job run automatically generates logs in CloudWatch Logs.

**AWS Console → AWS Glue → ETL Jobs → [job name] → Runs tab**

Click any run → **View CloudWatch logs** link.

Or navigate directly:
**CloudWatch Console → Log groups → `/aws-glue/jobs/output`**

**View logs via CLI:**
```bash
# Get the log group details for a specific run
aws glue get-job-runs --job-name silver-to-gold-job \
    --query "JobRuns[0].{Status:JobRunState,LogGroup:LogGroupName,Duration:ExecutionTime}"

# Tail job output logs (live follow)
aws logs tail /aws-glue/jobs/output --follow

# Get last 20 events from error log group
aws logs tail /aws-glue/jobs/error --follow
```

**Key log messages to verify success:**

```
Reading Silver: s3://customer-behavior-lakehouse1/silver/events/
Writing Gold: s3://customer-behavior-lakehouse1/gold/event_summary/
Registered Glue Catalog table: event_summary
Registered Glue Catalog table: daily_revenue
...
Silver to Gold job completed and Glue Catalog tables registered.
```

---

## 6.2 Set Up CloudWatch Alarms for Glue Jobs

**AWS Console → CloudWatch → Alarms → Create alarm**

### Alarm 1: Glue Job Failure Alert

| Field | Value |
|-------|-------|
| Metric namespace | Glue |
| Metric name | `glue.driver.aggregate.numFailedTasks` |
| Statistic | Sum |
| Period | 5 minutes |
| Threshold type | Static |
| Condition | `> 0` |
| Alarm name | `GlueJobFailure-Alert` |
| Notification | Create SNS topic → enter your email |

Click **Create alarm**.

**CLI alternative:**
```bash
# Step 1: Create SNS topic for alerts
SNS_ARN=$(aws sns create-topic --name lakehouse-alerts --query "TopicArn" --output text)
echo "SNS ARN: $SNS_ARN"

# Step 2: Subscribe your email (check inbox for confirmation)
aws sns subscribe \
    --topic-arn $SNS_ARN \
    --protocol email \
    --notification-endpoint your-email@example.com

# Step 3: Create Glue failure alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "GlueJobFailure-Alert" \
    --alarm-description "Alert when any Glue ETL job has failed tasks" \
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

## 6.3 Set Up CloudWatch Alarm for Athena

### Alarm 2: Athena Data Scan Cost Alert

Monitors total data scanned per day - alerts if approaching cost limits.

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "Athena-DataScan-Alert" \
    --alarm-description "Alert when Athena scans more than 5 GB in a day" \
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

> 💡 **FinOps note:** 5 GB threshold = $0.025 alert trigger. At Parquet efficiency, this threshold should rarely be hit during normal usage.

---

## 6.4 Monitor EC2 Instance Health

### Alarm 3: EC2 CPU High Alert

**CloudWatch Console → All metrics → EC2 → Per-Instance Metrics**

Select `lakehouse-dashboard` instance and view:
- **CPUUtilization** - should be low (~5–20%) at idle
- **NetworkIn/NetworkOut** - traffic from users accessing the dashboard

```bash
# Get your EC2 instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Create CPU high alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "EC2-CPU-High-Alert" \
    --alarm-description "EC2 CPU above 80% for 5 consecutive minutes" \
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

## 6.5 Create a CloudWatch Dashboard

Create a unified dashboard to view all pipeline health metrics in one place.

**CloudWatch Console → Dashboards → Create dashboard**

| Field | Value |
|-------|-------|
| Dashboard name | `lakehouse-pipeline-health` |

**Add widgets (manually or via JSON below):**

| Widget | Metric | Chart Type |
|--------|--------|-----------| 
| Glue Completed Tasks | `Glue / glue.driver.aggregate.numCompletedTasks` | Line |
| Glue Failed Tasks | `Glue / glue.driver.aggregate.numFailedTasks` | Line |
| Athena Data Scanned | `AWS/Athena / DataScannedInBytes` (Workgroup=lakehouse-wg) | Bar |
| EC2 CPU Utilization | `AWS/EC2 / CPUUtilization` (InstanceId=your-id) | Line |

**CLI to create dashboard:**
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

## 6.6 View Lambda Logs (Ingestion Path)

If you configured Lambda for Firehose transformation or batch DB extraction:

**CloudWatch Console → Log groups → `/aws/lambda/<function-name>`**

```bash
# List log streams
aws logs describe-log-streams \
    --log-group-name /aws/lambda/firehose-transform \
    --order-by LastEventTime \
    --descending \
    --query "logStreams[0].logStreamName" \
    --output text

# Get recent log events
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

## 6.7 Summary: Alarms Configured

| Alarm Name | Metric | Threshold | Action |
|------------|--------|-----------|--------|
| `GlueJobFailure-Alert` | `numFailedTasks` | > 0 | SNS email |
| `Athena-DataScan-Alert` | `DataScannedInBytes` | > 5 GB/day | SNS email |
| `EC2-CPU-High-Alert` | `CPUUtilization` | > 80% for 5 min | SNS email |

---

## 6.8 Test Alerting

Trigger a test alarm to verify SNS notifications are working:

```bash
# Force alarm into ALARM state (test only)
aws cloudwatch set-alarm-state \
    --alarm-name "GlueJobFailure-Alert" \
    --state-value ALARM \
    --state-reason "Manual test trigger from workshop"

# Check your email inbox for the SNS notification (arrives in ~1 minute)

# Reset back to OK after testing
aws cloudwatch set-alarm-state \
    --alarm-name "GlueJobFailure-Alert" \
    --state-value OK \
    --state-reason "Test complete - resetting alarm"
```

---

## 6.9 Check All Alarms Status

```bash
# View all lakehouse alarms and their current state
aws cloudwatch describe-alarms \
    --alarm-names "GlueJobFailure-Alert" "Athena-DataScan-Alert" "EC2-CPU-High-Alert" \
    --query "MetricAlarms[*].{Name:AlarmName,State:StateValue,Reason:StateReason}" \
    --output table
```

**Expected states:** All alarms should show `OK` state during normal pipeline operation.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| SNS email not received | Email subscription not confirmed | Check inbox for AWS confirmation email and click link |
| Alarm stays in `INSUFFICIENT_DATA` | No metric data yet | Run a Glue job or Athena query to generate metrics |
| Glue logs not appearing | Log group not yet created | Run at least one Glue job - logs appear after first run |
| Dashboard widgets show "No data" | Metric dimensions not matching | Verify instance ID and workgroup name in widget config |

✅ **Step 6 complete** - Your pipeline is fully monitored! Proceed to [Clean-up](../../5.5-Cleanup/) when you have finished exploring.
