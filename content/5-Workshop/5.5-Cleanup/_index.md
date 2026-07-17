---
title: "Clean-up"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5.5 </b> "
---

# Clean-up Resources

After completing the workshop, it is **critical** to delete all AWS resources to avoid ongoing charges. Follow this checklist in order - some resources depend on others being deleted first.

> ⚠️ **Important:** Skipping clean-up will result in ongoing charges. EC2 instances, Elastic IPs, and Glue ETL jobs that remain active will continue to bill your account.

**Estimated time:** 15–20 minutes

---

## Clean-up Order

Resources must be deleted in the following order to avoid dependency errors:

```
1. EC2 Instance (terminate)
2. Elastic IP (release)
3. Glue ETL Jobs (delete 3)
4. Glue Catalog Tables + Database (delete 7 tables, then database)
5. S3 Bucket (empty first, then delete)
6. CloudWatch Alarms + Dashboard + Log Groups
7. VPC + Subnet + IGW + Route Table + Security Group
8. IAM Roles (Glue role + EC2 role)
9. SNS Topic
10. Firehose Stream (if created)
```

---

## Step 1: Stop and Terminate EC2 Instance

> ⚠️ **Note:** Terminating deletes the EBS volume and all data on it. If you want to preserve your Streamlit app code, SCP the files to your local machine first:
> ```bash
> scp -i lakehouse-key.pem ec2-user@<elastic-ip>:~/app_beautiful.py ./app_beautiful.py
> ```

**AWS Console → EC2 → Instances → Select `lakehouse-dashboard`**
- **Instance state → Terminate instance** → Confirm

```bash
# Get instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Terminate instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID

# Verify termination (wait ~30 seconds)
aws ec2 describe-instances --instance-ids $INSTANCE_ID \
    --query "Reservations[0].Instances[0].State.Name"
# Expected: "terminated"
```

---

## Step 2: Release Elastic IP

> ⚠️ **Cost warning:** Elastic IPs that are allocated but not associated with a running instance are charged **$0.005/hour** (~$3.60/month). Release immediately after terminating the EC2 instance.

**AWS Console → EC2 → Elastic IPs → Select the IP → Actions → Release Elastic IP address**

```bash
# Find the allocation ID
aws ec2 describe-addresses \
    --query "Addresses[*].{IP:PublicIp,AllocId:AllocationId}" \
    --output table

# Release it (replace alloc-xxxxxxxxxx with actual ID)
aws ec2 release-address --allocation-id alloc-xxxxxxxxxx
```

---

## Step 3: Delete Glue ETL Jobs

**AWS Console → AWS Glue → ETL Jobs**

Select all three jobs → **Actions → Delete** → Confirm:
- `raw-to-bronze-job`
- `bronze-to-silver-job`
- `silver-to-gold-job`

```bash
aws glue delete-job --job-name raw-to-bronze-job
aws glue delete-job --job-name bronze-to-silver-job
aws glue delete-job --job-name silver-to-gold-job
echo "All Glue jobs deleted"
```

---

## Step 4: Delete Glue Data Catalog Tables and Database

**Delete tables first (required before deleting database):**

```bash
# Delete all 7 Gold tables
for table in event_summary daily_revenue payment_summary country_revenue device_summary source_summary dashboard_summary; do
    aws glue delete-table --database-name customer_behavior_catalog_db --name $table
    echo "Deleted table: $table"
done
```

**Then delete the database:**

```bash
aws glue delete-database --name customer_behavior_catalog_db
echo "Deleted Glue database"
```

---

## Step 5: Empty and Delete S3 Bucket

S3 buckets cannot be deleted unless they are completely empty (including all versions if versioning is enabled).

```bash
# Delete all current objects
aws s3 rm s3://customer-behavior-lakehouse1 --recursive
echo "All current objects deleted"

# Delete all versioned objects (if versioning was enabled)
aws s3api delete-objects \
    --bucket customer-behavior-lakehouse1 \
    --delete "$(aws s3api list-object-versions \
        --bucket customer-behavior-lakehouse1 \
        --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}' \
        --output json)"

# Delete all delete markers
aws s3api delete-objects \
    --bucket customer-behavior-lakehouse1 \
    --delete "$(aws s3api list-object-versions \
        --bucket customer-behavior-lakehouse1 \
        --query '{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' \
        --output json)"

# Now delete the bucket
aws s3 rb s3://customer-behavior-lakehouse1 --force
echo "S3 bucket deleted"
```

> 📌 **Tip:** If the bucket has many versioned objects, use the S3 Console instead:
> S3 → Select bucket → **Empty** → type "permanently delete" → **Empty**
> Then: **Delete** → type bucket name → **Delete bucket**

---

## Step 6: Delete CloudWatch Alarms, Dashboard, and Log Groups

```bash
# Delete alarms
aws cloudwatch delete-alarms \
    --alarm-names "GlueJobFailure-Alert" "Athena-DataScan-Alert" "EC2-CPU-High-Alert"
echo "CloudWatch alarms deleted"

# Delete CloudWatch dashboard
aws cloudwatch delete-dashboards --dashboard-names "lakehouse-pipeline-health"
echo "CloudWatch dashboard deleted"

# Delete Glue job log groups
aws logs delete-log-group --log-group-name /aws-glue/jobs/output
aws logs delete-log-group --log-group-name /aws-glue/jobs/error

# Delete Lambda log groups (if created)
aws logs delete-log-group --log-group-name /aws/lambda/firehose-transform 2>/dev/null || true
echo "Log groups deleted"
```

---

## Step 7: Delete VPC and Networking Resources

Delete in this exact order (dependencies must be removed first):

```bash
# Get resource IDs
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=lakehouse-vpc" \
    --query "Vpcs[0].VpcId" --output text)

IGW_ID=$(aws ec2 describe-internet-gateways \
    --filters "Name=tag:Name,Values=lakehouse-igw" \
    --query "InternetGateways[0].InternetGatewayId" --output text)

RT_ID=$(aws ec2 describe-route-tables \
    --filters "Name=tag:Name,Values=lakehouse-rt" \
    --query "RouteTables[0].RouteTableId" --output text)

SUBNET_ID=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=lakehouse-public-subnet" \
    --query "Subnets[0].SubnetId" --output text)

SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=lakehouse-ec2-sg" \
    --query "SecurityGroups[0].GroupId" --output text)

# 1. Delete Security Group
aws ec2 delete-security-group --group-id $SG_ID
echo "Security Group deleted"

# 2. Delete custom Route Table (if separate from main)
[ ! -z "$RT_ID" ] && aws ec2 delete-route-table --route-table-id $RT_ID && echo "Route Table deleted"

# 3. Detach and delete Internet Gateway
aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID
echo "Internet Gateway deleted"

# 4. Delete Subnet
aws ec2 delete-subnet --subnet-id $SUBNET_ID
echo "Subnet deleted"

# 5. Delete VPC (must be last)
aws ec2 delete-vpc --vpc-id $VPC_ID
echo "VPC deleted"
```

---

## Step 8: Delete IAM Roles

```bash
# --- Delete Glue ETL Role ---
# Detach managed policies
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam detach-role-policy \
    --role-name AWSGlueServiceRole-lakehouse \
    --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess

# Delete Glue role
aws iam delete-role --role-name AWSGlueServiceRole-lakehouse
echo "Glue IAM role deleted"

# --- Delete EC2 Dashboard Role ---
aws iam detach-role-policy \
    --role-name lakehouse-ec2-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess
aws iam detach-role-policy \
    --role-name lakehouse-ec2-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Delete EC2 role
aws iam delete-role --role-name lakehouse-ec2-role
echo "EC2 IAM role deleted"
```

---

## Step 9: Delete SNS Topic

```bash
# Find SNS topic ARN
SNS_ARN=$(aws sns list-topics \
    --query "Topics[?contains(TopicArn,'lakehouse')].TopicArn" \
    --output text)

# Delete SNS topic (unsubscribes all endpoints)
[ ! -z "$SNS_ARN" ] && aws sns delete-topic --topic-arn $SNS_ARN && echo "SNS topic deleted"
```

---

## Step 10: Delete Firehose Stream (If Created)

```bash
aws firehose delete-delivery-stream --delivery-stream-name lakehouse-event-stream 2>/dev/null && \
    echo "Firehose stream deleted" || echo "Firehose stream not found (skipped)"
```

---

## Final Verification

Run this comprehensive check for any remaining billable resources:

```bash
echo "========================================="
echo "=== Checking for remaining resources ==="
echo "========================================="

echo ""
echo "--- Running EC2 Instances ---"
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running,stopped" \
    --query "Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[?Key=='Name'].Value|[0]}" \
    --output table

echo ""
echo "--- Allocated Elastic IPs ---"
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
echo "Expected: All sections above should show NO resources"
echo "========================================="
```

**Expected output:** All sections should be empty (no remaining resources).

---

## Clean-up Summary Checklist

Complete this checklist to confirm everything is deleted:

-  EC2 instance `lakehouse-dashboard` terminated
-  Elastic IP released
-  `raw-to-bronze-job` deleted
-  `bronze-to-silver-job` deleted
-  `silver-to-gold-job` deleted
-  7 Glue Catalog tables deleted
-  Glue database `customer_behavior_catalog_db` deleted
-  S3 bucket `customer-behavior-lakehouse1` emptied and deleted
-  CloudWatch alarm `GlueJobFailure-Alert` deleted
-  CloudWatch alarm `Athena-DataScan-Alert` deleted
-  CloudWatch alarm `EC2-CPU-High-Alert` deleted
-  CloudWatch dashboard `lakehouse-pipeline-health` deleted
-  CloudWatch log groups deleted
-  Security Group `lakehouse-ec2-sg` deleted
-  Route Table deleted (or cleaned up)
-  Internet Gateway `lakehouse-igw` deleted
-  Subnet `lakehouse-public-subnet` deleted
-  VPC `lakehouse-vpc` deleted
-  IAM role `AWSGlueServiceRole-lakehouse` deleted
-  IAM role `lakehouse-ec2-role` deleted
-  SNS topic `lakehouse-alerts` deleted
-  Firehose stream `lakehouse-event-stream` deleted (if created)

✅ **Workshop complete!** All resources cleaned up. No further charges will be incurred.

---

## Congratulations!

Successfully completed the **FinOps-Optimized Serverless Medallion Data Lakehouse** workshop. Built a complete end-to-end data analytics pipeline on AWS that:

- ✅ Ingests streaming events (Firehose) and batch CSV data (Lambda)
- ✅ Processes data through 4 Medallion tiers: Raw → Bronze → Silver → Gold
- ✅ Queries business KPIs serverlessly with Amazon Athena
- ✅ Visualizes insights in a Streamlit dashboard on EC2
- ✅ Monitors the pipeline with CloudWatch alarms
- ✅ Keeps cost minimal with FinOps best practices (Parquet, serverless, pay-per-use)
