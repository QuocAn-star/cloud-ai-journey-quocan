---
title: "Workshop"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# FinOps-Optimized Serverless Medallion Data Lakehouse - Workshop

## About This Workshop

This hands-on workshop walks you through building a **cloud-native, fully serverless data lakehouse** on AWS from scratch. You will implement a complete data pipeline that ingests, transforms, and visualizes customer behavior data using the **Medallion Architecture** (Raw → Bronze → Silver → Gold), following **FinOps best practices** to keep costs minimal throughout.

By the end of this workshop, you will have a fully working end-to-end pipeline running on your own AWS account.

## What You Will Build

```
Website/Mobile Events
        │
        ▼
  API Gateway ──► Firehose ──► Lambda (inline transform)
                                       │
                                       ▼
                                  S3: Raw/Streaming
                                       │
  E-commerce DB ──► EventBridge ──► Lambda ──► S3: Raw/Batch
                                       │
                              ┌────────┘
                              ▼
                      AWS Glue ETL Job 1
                      (Raw → Bronze: CSV to Parquet)
                              │
                              ▼
                      AWS Glue ETL Job 2
                      (Bronze → Silver: Cleanse, Deduplicate)
                              │
                              ▼
                      AWS Glue ETL Job 3
                      (Silver → Gold: Business Aggregations)
                              │
                        ┌─────┘
                        ▼
                  Glue Data Catalog
                        │
                        ▼
                  Amazon Athena (SQL Query)
                        │
                        ▼
              Streamlit Dashboard (EC2 + VPC)
```

## Workshop Sections

1. [Overview](5.1-Overview/)
2. [Prerequisite](5.2-Prerequisite/)
3. [Architecture Description](5.3-Architecture/)
4. [Hands-On Steps](5.4-Steps/)
   - [Step 1: VPC & Networking Setup](5.4-Steps/5.4.1-VPC/)
   - [Step 2: S3 Buckets & Storage Setup](5.4-Steps/5.4.2-S3/)
   - [Step 3: AWS Glue ETL Jobs](5.4-Steps/5.4.3-Glue/)
   - [Step 4: Amazon Athena Queries](5.4-Steps/5.4.4-Athena/)
   - [Step 5: Deploy Streamlit Dashboard on EC2](5.4-Steps/5.4.5-EC2-Dashboard/)
   - [Step 6: Monitoring with CloudWatch](5.4-Steps/5.4.6-Monitoring/)
5. [Clean-up](5.5-Cleanup/)

## Estimated Time & Cost

| Item | Value |
|------|-------|
| **Duration** | ~3–4 hours (full workshop) |
| **Estimated Cost** | ~$1–3 USD (if cleaned up same day) |
| **AWS Region** | `us-east-1` (N. Virginia) - recommended |
| **Difficulty** | Intermediate |