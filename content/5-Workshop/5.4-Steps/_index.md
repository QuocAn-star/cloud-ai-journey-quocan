---
title: "Hands-On Steps"
date: 2024-01-01
weight: 4
chapter: false
pre: " <b> 5.4 </b> "
---

# Hands-On Steps

This section walks you through the complete end-to-end implementation of the **FinOps-Optimized Serverless Medallion Data Lakehouse** on AWS.

---

## Step Overview

| Step | Topic | Time | Key Output |
|------|-------|------|-----------|
| [5.4.1 VPC & Networking](5.4.1-VPC/) | Create VPC, subnet, IGW, security group | 15–20 min | `lakehouse-vpc` ready for EC2 |
| [5.4.2 S3 & Data Upload](5.4.2-S3/) | Create S3 bucket, folder structure, upload CSV data | 20–30 min | 6 CSV files in `raw/`, IAM role for Glue |
| [5.4.3 AWS Glue ETL](5.4.3-Glue/) | Create 3 ETL jobs: Raw→Bronze→Silver→Gold | 30–40 min | 7 Gold tables registered in Glue Catalog |
| [5.4.4 Amazon Athena](5.4.4-Athena/) | Configure Athena, run 7 business queries | 15–20 min | Verified query results |
| [5.4.5 EC2 & Dashboard](5.4.5-EC2-Dashboard/) | Launch EC2, deploy Streamlit dashboard | 25–35 min | Live dashboard at `http://<ip>:8501` |
| [5.4.6 Monitoring](5.4.6-Monitoring/) | Set up CloudWatch alarms and dashboard | 20–25 min | 3 alarms + monitoring dashboard |

**Total estimated time:** 2–3 hours for all steps

---

## Important: Run Steps in Order

Each step builds on the previous one. Do not skip steps.

```
[5.4.1 VPC]          → provides network for EC2
    ↓
[5.4.2 S3 + IAM]     → provides data and roles for Glue
    ↓
[5.4.3 Glue ETL]     → produces Gold tables in Glue Catalog
    ↓
[5.4.4 Athena]       → validates Gold data via SQL
    ↓
[5.4.5 EC2 Dashboard]→ visualizes Athena Gold data
    ↓
[5.4.6 Monitoring]   → observes entire pipeline
```

---

## Start with Step 1

→ [Step 1: VPC & Networking Setup](5.4.1-VPC/)
