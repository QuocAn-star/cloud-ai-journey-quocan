---
title: "Overview"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 5.1 </b> "
---

# Workshop Overview

## What Is This Workshop About?

This workshop guides you through building a **FinOps-Optimized Serverless Medallion Data Lakehouse** on AWS - a production-grade data analytics platform designed for e-commerce customer behavior analysis.

The core idea is to demonstrate how modern e-commerce businesses can gain **deep analytics insights** (sales trends, customer segmentation, payment analysis, traffic source performance) from two data sources:

1. **Real-time clickstream events** from web and mobile apps (streaming path via API Gateway → Firehose → S3)
2. **Transactional order records** from an e-commerce database (batch path via EventBridge → Lambda → S3)

...all while keeping the infrastructure **100% serverless** and the monthly bill under **$3/day** of actual usage.

---

## Business Context

Imagine you are the data engineer at a growing e-commerce company. Your business stakeholders ask:

- *"Which countries generate the most revenue?"*
- *"Which payment method do our customers prefer?"*
- *"Which device type drives the most orders - mobile, desktop, or tablet?"*
- *"How did our daily revenue trend over the past year?"*
- *"What are the most frequent user events on our platform?"*

Without a proper data platform, answering these questions requires manually exporting CSV files, running ad-hoc SQL against the production database, or building expensive always-on data warehouse clusters.

This workshop builds the platform that answers all these questions - automatically, reliably, and cost-efficiently - using AWS managed services.

---

## Learning Outcomes

After completing this workshop, you will be able to:

| Skill | What You Will Learn |
|-------|-------------------|
| **VPC & Networking** | Create VPC, Subnets, Internet Gateway, Route Tables, Security Groups for a secure data platform |
| **S3 Data Lake** | Design a multi-tier S3 structure (Raw → Bronze → Silver → Gold) with proper bucket policies |
| **AWS Glue ETL** | Write PySpark ETL jobs that transform data across Medallion tiers |
| **Glue Data Catalog** | Register table schemas programmatically - no manual crawlers needed |
| **Amazon Athena** | Run serverless SQL queries on S3 data using the Glue Data Catalog |
| **Streamlit on EC2** | Deploy a Python web dashboard on EC2 within a VPC |
| **CloudWatch Monitoring** | Set up alarms and dashboards for pipeline observability |
| **IAM Security** | Apply least-privilege IAM roles to each service |
| **FinOps** | Understand how Parquet format reduces Athena query costs |

---

## Architecture Summary

The platform is built across **6 functional layers**:

```
┌─────────────────────────────────────────────────────────┐
│  DATA SOURCES                                           │
│  • Website/Mobile → real-time JSON events               │
│  • E-commerce DB  → periodic CSV batch exports          │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  INGESTION LAYER                                        │
│  • API Gateway → Firehose → Lambda → S3 (streaming)    │
│  • EventBridge → Lambda (DB extract) → S3 (batch)      │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  STORAGE LAYER - MEDALLION ARCHITECTURE                 │
│  S3: Raw → Bronze (Parquet) → Silver (clean) → Gold    │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  PROCESSING LAYER                                       │
│  • Glue ETL Job 1: Raw → Bronze (CSV to Parquet)       │
│  • Glue ETL Job 2: Bronze → Silver (cleanse/dedup)     │
│  • Glue ETL Job 3: Silver → Gold (KPI aggregations)    │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  QUERY LAYER                                            │
│  • Glue Data Catalog (metadata registry)               │
│  • Amazon Athena (serverless SQL on S3)                │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  VISUALIZATION LAYER                                    │
│  • Streamlit Dashboard on EC2 (within VPC)             │
│  • Connects to Athena via aws-wrangler + boto3         │
└─────────────────────────────────────────────────────────┘
```

---

## AWS Services Used

| Service | Role in This Workshop |
|---------|----------------------|
| **Amazon VPC** | Isolated network for EC2 and data platform |
| **Public Subnet** | Subnet hosting EC2 Dashboard |
| **Internet Gateway** | Enable internet access for EC2 |
| **Route Table** | Route traffic from subnet to Internet Gateway |
| **Security Group** | Allow inbound port 8501 (Streamlit) + SSH |
| **Amazon S3** | Four-tier data lake (Raw, Bronze, Silver, Gold) |
| **Amazon Data Firehose** | Buffer and deliver streaming events to S3 |
| **Amazon API Gateway** | HTTP endpoint for client event ingestion |
| **AWS Lambda** | Inline Firehose transformation + DB extraction |
| **Amazon EventBridge Scheduler** | Trigger batch Lambda on schedule |
| **AWS Glue** | PySpark ETL jobs for data transformation |
| **AWS Glue Data Catalog** | Metadata registry for Athena tables |
| **Amazon Athena** | Serverless SQL queries on S3 Gold layer |
| **Amazon EC2** | Host Streamlit dashboard |
| **Amazon EBS** | Persistent storage for EC2 instance |
| **Elastic IP** | Static IP for EC2 instance |
| **AWS IAM** | Least-privilege roles per service |
| **Amazon CloudWatch** | Logs, metrics, and alarms |
| **AWS KMS** | At-rest encryption for S3 buckets |

---

## Source Code Files

All source code used in this workshop is available in the `source_code/` directory:

| File | Description |
|------|-------------|
| `raw_to_bronze_job.py` | Glue ETL Job 1: Read CSV + streaming JSON from Raw, write Parquet to Bronze |
| `bronze_to_silver_job.py` | Glue ETL Job 2: Deduplicate, cleanse, normalize column names → Silver |
| `silver_to_gold_job.py` | Glue ETL Job 3: Business KPI aggregations → Gold; auto-register Glue Catalog tables |
| `athena_create_tables.sql` | SQL statements to create external tables in Athena (manual fallback) |
| `athena_queries.sql` | Sample business queries to run on Gold layer |
| `app_beautiful.py` | Streamlit dashboard application connecting to Athena via aws-wrangler |

---

## Final Dashboard Result

The end result of this workshop is a fully interactive analytics dashboard running on EC2:

![Revenue Trend Dashboard](/result/DashBoard/Revenue%20Trend.png)

![Top Performers](/result/DashBoard/Top%20Performers.jpg)

![Event Distribution](/result/DashBoard/Event%20Distribution.png)

---

## Estimated Time & Cost

| Item | Value |
|------|-------|
| **Duration** | ~3–4 hours (full workshop) |
| **Estimated Cost** | ~$1–3 USD (if cleaned up same day) |
| **AWS Region** | `us-east-1` (N. Virginia) - recommended |
| **Difficulty** | Intermediate |

> 💡 **FinOps Tip:** The total cost is kept low because all compute services (Glue, Athena, Lambda, Firehose) are pay-per-use - you only pay when they run. The EC2 instance (t3.micro) is Free Tier eligible for the first 12 months.

---

## Navigation

Proceed to the next sections in order:

1. ✅ **5.1 Overview** ← You are here
2. → [5.2 Prerequisite](../5.2-Prerequisite/)
3. → [5.3 Architecture Description](../5.3-Architecture/)
4. → [5.4 Hands-On Steps](../5.4-Steps/)
5. → [5.5 Clean-up](../5.5-Cleanup/)
