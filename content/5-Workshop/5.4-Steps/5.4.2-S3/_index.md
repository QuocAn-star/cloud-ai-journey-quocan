---
title: "Step 2: S3 & Data Upload"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

# Step 2: S3 Buckets & Data Upload

In this step, you will create the S3 bucket with the Medallion Architecture prefix structure, configure encryption, and upload the sample data files to the Raw tier.

**Estimated time:** 20–30 minutes

---

## Prerequisites

- AWS CLI configured with `AmazonS3FullAccess` and `IAMFullAccess`
- Sample CSV data files ready (see Section 5.2 for generation script)

---

## 2.1 Create the S3 Bucket

**AWS Console → S3 → Create bucket**

| Field | Value |
|-------|-------|
| Bucket name | `customer-behavior-lakehouse1` |
| AWS Region | `us-east-1` |
| Object Ownership | ACLs disabled (recommended) |
| Block all public access | ✅ Enabled (keep all blocks on) |
| Bucket versioning | Enable (recommended for data recovery) |
| Default encryption | Server-side encryption with Amazon S3 managed keys (SSE-S3) |

Click **Create bucket**.

> 💡 **Note:** S3 bucket names are globally unique. If `customer-behavior-lakehouse1` is taken, append your AWS account ID: `customer-behavior-lakehouse1-<account-id>`. Update all references in the ETL scripts accordingly.

**CLI alternative:**
```bash
aws s3api create-bucket \
    --bucket customer-behavior-lakehouse1 \
    --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket customer-behavior-lakehouse1 \
    --versioning-configuration Status=Enabled

# Enable encryption (SSE-S3)
aws s3api put-bucket-encryption \
    --bucket customer-behavior-lakehouse1 \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

---

## 2.2 Create the Folder Structure (S3 Prefixes)

Inside the bucket, create the following top-level "folders" (S3 prefixes):

```bash
# Create all required prefixes
aws s3api put-object --bucket customer-behavior-lakehouse1 --key raw/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key bronze/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key silver/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key gold/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key athena-results/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key scripts/
aws s3api put-object --bucket customer-behavior-lakehouse1 --key tmp/
```

Or via Console: In the bucket, click **Create folder** for each of: `raw`, `bronze`, `silver`, `gold`, `athena-results`, `scripts`, `tmp`.

---

## 2.3 Upload Sample Data Files to Raw Tier

Upload all 6 CSV files to the `raw/` prefix:

```bash
# Upload each CSV file to S3 Raw
aws s3 cp customers.csv    s3://customer-behavior-lakehouse1/raw/customers.csv
aws s3 cp orders.csv       s3://customer-behavior-lakehouse1/raw/orders.csv
aws s3 cp products.csv     s3://customer-behavior-lakehouse1/raw/products.csv
aws s3 cp order_items.csv  s3://customer-behavior-lakehouse1/raw/order_items.csv
aws s3 cp reviews.csv      s3://customer-behavior-lakehouse1/raw/reviews.csv
aws s3 cp sessions.csv     s3://customer-behavior-lakehouse1/raw/sessions.csv

# Verify all uploads succeeded
aws s3 ls s3://customer-behavior-lakehouse1/raw/
```

**Expected output:**
```
2026-07-06 10:00:00    350000 customers.csv
2026-07-06 10:00:01   1200000 orders.csv
2026-07-06 10:00:01    220000 products.csv
2026-07-06 10:00:02    450000 order_items.csv
2026-07-06 10:00:02    180000 reviews.csv
2026-07-06 10:00:03    320000 sessions.csv
```

![S3 Raw - CSV files uploaded (original source data)](/result/S3/S3%20Raw%20-%20d%E1%BB%AF%20li%E1%BB%87u%20g%E1%BB%91c.jpg)

---

## 2.4 Test Firehose Streaming Ingestion (Optional)

If you want to test the streaming path via Firehose:

**Step A: Create a Firehose Delivery Stream**

**AWS Console → Amazon Data Firehose → Create Firehose stream**

| Field | Value |
|-------|-------|
| Source | Direct PUT |
| Destination | Amazon S3 |
| Firehose stream name | `lakehouse-event-stream` |
| S3 bucket | `customer-behavior-lakehouse1` |
| S3 prefix | `raw/streaming/events/!{timestamp:yyyy}/!{timestamp:MM}/!{timestamp:dd}/!{timestamp:HH}/` |
| S3 error prefix | `raw/streaming/errors/` |
| Buffer size | 1 MB |
| Buffer interval | 60 seconds |

**Step B: Send a test event**

```bash
aws firehose put-record \
    --delivery-stream-name lakehouse-event-stream \
    --record '{
        "Data": "{\"event_type\": \"page_view\", \"customer_id\": \"CUST-0001\", \"product_id\": \"PROD-042\", \"timestamp\": \"2026-07-10T10:00:00Z\"}\n"
    }'
```

**Step C: Wait and verify**

Wait 60–90 seconds (Firehose buffer interval), then verify data appeared in S3:

```bash
aws s3 ls s3://customer-behavior-lakehouse1/raw/streaming/ --recursive
```

![Firehose streaming data delivered to S3 raw/streaming/](/result/S3/FirehoseStreaming%20%C4%91%C3%A3%20%C4%91%E1%BB%95%20data%20v%C3%A0o%20S3.jpg)

---

## 2.5 Create IAM Role for Glue ETL Jobs

Create an IAM role that Glue ETL jobs will use to read from and write to S3.

**AWS Console → IAM → Roles → Create role**

| Field | Value |
|-------|-------|
| Trusted entity type | AWS service |
| Service | Glue |
| Use case | Glue |

**Add permissions - attach these policies:**
- `AWSGlueServiceRole` (managed) - allows Glue to write CloudWatch logs
- `AmazonS3FullAccess` - for workshop simplicity
- `AmazonAthenaFullAccess` - for Glue → Catalog registration in `silver_to_gold_job`

**Role name:** `AWSGlueServiceRole-lakehouse`

> ⚠️ **Least-privilege note:** In production, replace broad managed policies with a custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/raw/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/bronze/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/silver/*",
        "arn:aws:s3:::customer-behavior-lakehouse1"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:DeleteObject"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/bronze/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/silver/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/gold/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/scripts/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/tmp/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:*", "athena:*"],
      "Resource": "*"
    }
  ]
}
```

---

## 2.6 Upload ETL Scripts to S3

Upload the three Glue ETL scripts so Glue can access them:

```bash
# Upload all scripts
aws s3 cp source_code/raw_to_bronze_job.py    s3://customer-behavior-lakehouse1/scripts/raw_to_bronze_job.py
aws s3 cp source_code/bronze_to_silver_job.py s3://customer-behavior-lakehouse1/scripts/bronze_to_silver_job.py
aws s3 cp source_code/silver_to_gold_job.py   s3://customer-behavior-lakehouse1/scripts/silver_to_gold_job.py

# Verify
aws s3 ls s3://customer-behavior-lakehouse1/scripts/
```

---

## 2.7 Validation

```bash
# List all prefixes to confirm structure
echo "=== S3 Bucket Structure ==="
aws s3 ls s3://customer-behavior-lakehouse1/

# Check raw/ contains all 6 CSV files
echo "=== Raw CSV files ==="
aws s3 ls s3://customer-behavior-lakehouse1/raw/

# Check bucket versioning
echo "=== Versioning ==="
aws s3api get-bucket-versioning --bucket customer-behavior-lakehouse1

# Check encryption
echo "=== Encryption ==="
aws s3api get-bucket-encryption --bucket customer-behavior-lakehouse1 \
    --query "ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm"
```

**Expected output:**
- 7 prefixes visible: `raw/`, `bronze/`, `silver/`, `gold/`, `athena-results/`, `scripts/`, `tmp/`
- 6 CSV files in `raw/`
- Versioning: `{ "Status": "Enabled" }`
- Encryption: `"AES256"`

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `BucketAlreadyExists` | Bucket name taken globally | Use unique name: add account ID suffix |
| `AccessDenied` on upload | Missing S3 write permissions | Attach `AmazonS3FullAccess` to your IAM user |
| Firehose data not appearing in S3 | Buffer interval not elapsed | Wait 60–90 seconds |
| Script upload fails | Missing `scripts/` prefix | Run `aws s3api put-object --bucket ... --key scripts/` first |

✅ **Step 2 complete** - Proceed to [Step 3: AWS Glue ETL Jobs](../5.4.3-Glue/)
