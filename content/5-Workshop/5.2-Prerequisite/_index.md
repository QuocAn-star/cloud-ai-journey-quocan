---
title: "Prerequisite"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 5.2 </b> "
---

# Prerequisite

Before starting this workshop, please ensure you have the following ready.

---

## 1. AWS Account

- An active **AWS account** with billing enabled
- Recommended: Create a dedicated IAM user instead of using the root account
- **AWS Region**: Use `us-east-1` (N. Virginia) throughout this workshop for consistency

> 💡 **Tip:** If you are using an AWS promotional credit account (such as from FCAJ), check your remaining credit balance before starting.

---

## 2. IAM Permissions Required

Your IAM user or role must have permissions for the following services. For simplicity during this workshop, you can attach the following AWS managed policies:

| AWS Managed Policy | Services Covered |
|-------------------|--------------------|
| `AmazonS3FullAccess` | S3 bucket creation, read/write |
| `AWSGlueConsoleFullAccess` | Glue ETL jobs, Data Catalog |
| `AmazonAthenaFullAccess` | Athena query execution |
| `AmazonEC2FullAccess` | EC2, VPC, Security Groups, Elastic IP |
| `AWSLambda_FullAccess` | Lambda function creation |
| `AmazonAPIGatewayAdministrator` | API Gateway configuration |
| `CloudWatchFullAccess` | Logs, metrics, alarms |
| `AWSKeyManagementServicePowerUser` | KMS key creation and usage |
| `IAMFullAccess` | Create IAM roles for services |

> ⚠️ **Note:** In production, you should apply least-privilege policies instead of full access. The above is for workshop convenience only.

---

## 3. Tools & Software

### AWS CLI v2

Install and configure the AWS CLI v2:

```bash
# Verify installation
aws --version
# Expected output: aws-cli/2.x.x

# Configure credentials
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Verify configuration works
aws sts get-caller-identity
# Expected: your Account ID and IAM user/role ARN
```

### Python 3.9+

```bash
python --version
# Expected: Python 3.9.x or higher
```

### Required Python packages (for local testing):

```bash
pip install boto3 pandas streamlit plotly awswrangler pyathena
```

### Git (optional, for source code management):

```bash
git --version
```

---

## 4. Sample Data Files

This workshop uses synthetic e-commerce data. You need the following CSV files to upload to S3:

| File | Columns | Description |
|------|---------|-------------|
| `customers.csv` | customer_id, name, email, country, signup_date | Customer master data |
| `orders.csv` | order_id, customer_id, total_usd, payment_method, device, source, country, order_time | Order transactions |
| `products.csv` | product_id, name, category, price_usd | Product catalog |
| `order_items.csv` | item_id, order_id, product_id, quantity, price_usd | Line items per order |
| `reviews.csv` | review_id, order_id, rating, comment, review_date | Customer reviews |
| `sessions.csv` | session_id, customer_id, start_time, end_time, device, source | Web/app session data |

You can generate synthetic data using Python:

```python
import pandas as pd
import random
from datetime import datetime, timedelta

# Generate sample orders (10,000 records)
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
print("Generated orders.csv with 10,000 records")
```

---

## 5. Estimated Cost Breakdown

| Service | Workshop Usage | Estimated Cost |
|---------|---------------|----------------|
| EC2 t3.micro | 4–5 hours | ~$0.05 |
| S3 storage | ~500 MB total | ~$0.01 |
| Glue ETL (3 jobs) | 3 × 2 DPUs × 5 min | ~$0.15 |
| Athena queries | ~10 queries × 50 MB | ~$0.00 |
| API Gateway | ~100 test requests | ~$0.00 |
| Data Firehose | ~1 MB test data | ~$0.00 |
| CloudWatch | Default metrics | ~$0.00 |
| **Total** | | **~$0.21–$0.50** |

> 💡 **FinOps tip:** Always clean up resources after the workshop (see Section 5.5) to avoid ongoing charges.

---

## 6. Knowledge Prerequisites

You should have basic familiarity with:

- **AWS Console navigation** - creating and viewing resources
- **Python basics** - reading and understanding PySpark/Pandas code
- **SQL basics** - SELECT, GROUP BY, ORDER BY statements
- **Networking concepts** - what a VPC, subnet, and security group are
- **S3 basics** - creating buckets and uploading files

No prior experience with Glue, Athena, or Streamlit is required - this workshop teaches them from scratch.

---

## Pre-flight Checklist

Before proceeding to Step 1, confirm all items below:

-  AWS account is active with billing enabled
-  IAM user/role has necessary permissions listed above
-  AWS CLI v2 installed and configured (`aws sts get-caller-identity` returns your account ID)
-  Python 3.9+ installed
-  Sample CSV data files ready (or generated using the script above)
-  AWS Region set to `us-east-1`

✅ **All checked?** Proceed to [Architecture Description](../5.3-Architecture/)
