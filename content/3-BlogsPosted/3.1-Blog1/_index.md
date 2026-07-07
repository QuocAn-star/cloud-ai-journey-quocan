---
title: "Blog 1"
date: 2026-01-01
weight: 1
chapter: false
pre: " <b> 3.1. </b> "
---

# Building a Real-time CDC Pipeline: From Amazon Aurora to Amazon S3 Tables with Debezium and Firehose

> **Original article:** [Real-time CDC from Aurora PostgreSQL to Amazon S3 Tables using Debezium and Firehose](https://aws.amazon.com/blogs/big-data/real-time-cdc-from-aurora-postgresql-to-amazon-s3-tables-using-debezium-and-firehose/)

> **Translation:** [Real-time CDC from Aurora PostgreSQL to Amazon S3 Tables using Debezium and Firehose](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2199216520843308/?rdid=AAZBwZqs23GM5W9s#)

---

In today's data era, separating transactional (OLTP) and analytical (OLAP) data is critically important. Running heavy analytical queries directly on an Amazon Aurora cluster will almost certainly degrade transactional system performance.

Traditionally, batch export is the go-to approach - but it introduces significant latency. This article introduces a more powerful solution: **Real-time Change Data Capture (CDC)** to move data from Aurora PostgreSQL to **Amazon S3 Tables** in Apache Iceberg format, keeping data always ready for immediate query.

---

## 1. Why Amazon S3 Tables and Apache Iceberg?

Unlike traditional CDC methods that only log changes in append-only fashion, the **Apache Iceberg** format supports row-level **update** and **delete** operations.

**Amazon S3 Tables** also automates complex maintenance tasks like snapshot management and data compaction, freeing up data engineers from operational toil. You can also leverage Iceberg's **Time Travel** feature to query data at a specific point in the past.

---

## 2. System Architecture: 6 Core Components

The system is optimized with 6 data transmission steps:

| Step | From → To | Description |
|------|-----------|-------------|
| 1 | Aurora PostgreSQL → Debezium | Debezium on MSK Connect reads changes from PostgreSQL WAL with minimal performance impact |
| 2 | Debezium → Amazon MSK | `ByLogicalTableRouter` merges changes from multiple tables into one Kafka topic - reducing cost and operational complexity |
| 3 | Amazon MSK → Firehose | Amazon Data Firehose continuously polls data from MSK via AWS PrivateLink |
| 4 | AWS Lambda | The "transformation brain" - decodes data, flattens Debezium's complex structure, and attaches metadata (table name + operation type) |
| 5 | Firehose → S3 Tables | Firehose uses Lambda metadata to push data into the correct Iceberg table in S3 |
| 6 | Query & Governance | Data is ready for query via Amazon Athena or Redshift, governed by AWS Lake Formation |

---

## 3. The Intelligent Data Transformation Mechanism

The most interesting aspect of this solution is how Lambda maps Debezium operation codes to Firehose:

| Debezium Code | Meaning | Firehose Operation |
|---|---|---|
| `c` (Create) / `r` (Read) | Insert | → **Insert** into Iceberg table |
| `u` (Update) | Update | → **Upsert** based on primary key |
| `d` (Delete) | Delete | → **Delete** the corresponding row |

Thanks to this mechanism, the destination table in S3 Tables is always a **perfect replica** of the current state of the source database.

---

## 4. Rapid Deployment with AWS CDK

Instead of manually configuring each service, you can deploy the entire infrastructure as code using **AWS CDK**. The process includes:

1. Enable `logical_replication` on Aurora.
2. Package and register the Debezium plugin on MSK Connect.
3. Use `cdk deploy` to instantiate all **6 resource stacks** - from the MSK cluster to the S3 Tables bucket.

This solution helps you build a near-real-time **Data Lakehouse** that is highly cost-optimized by merging multiple tables into a single data stream. If you're looking for a modern way to synchronize transactional data for analytics, this is the answer.

---

## Key Takeaways

- **CDC + Iceberg = Real-time analytics without query pressure on Aurora**
- Merging multiple tables into one Kafka topic significantly reduces cost
- Lambda is the bridge between Debezium's format and Firehose's expectations
- AWS CDK makes this entire infrastructure reproducible and version-controlled

---

*Blog image:*

![Blog 1 - Real-time CDC Pipeline](/images/blog1.jpg)
