---
title: "Day 4"
date: 2026-04-23
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
---

> **Day 4 - Big Data Analytics on AWS:** Exploring Amazon EMR, Amazon Kinesis, Amazon Data Firehose, AWS Lake Formation, Amazon Redshift, and Amazon QuickSight to understand how AWS services work together in a modern data analytics platform.

---

## Objectives

- Understand the architecture of a modern data analytics platform on AWS.
- Learn how real-time streaming data is ingested using Amazon Kinesis.
- Explore Amazon Data Firehose for automated data delivery.
- Understand the role of Amazon EMR in large-scale data processing.
- Learn centralized data governance using AWS Lake Formation.
- Compare Amazon Redshift and Amazon Athena for analytical workloads.
- Visualize business data using Amazon QuickSight.

---

# Modern Data Analytics Architecture

The final day focused on understanding how multiple AWS services integrate into a complete analytics platform.

A typical modern data pipeline consists of the following stages:

```
Data Source
      ↓
Amazon Kinesis Data Streams
      ↓
Amazon Data Firehose
      ↓
Amazon S3
      ↓
AWS Glue Data Catalog
      ↓
Amazon Athena
      ↓
Amazon Redshift
      ↓
Amazon QuickSight
```

This architecture demonstrates the complete lifecycle of enterprise data, from ingestion and storage to processing, analytics, and visualization.

---

# Amazon EMR

The first service introduced was **Amazon EMR (Elastic MapReduce)**, AWS's managed big data processing platform.

Amazon EMR supports popular open-source frameworks such as:

- Apache Spark
- Apache Hadoop
- Apache Hive
- Apache Presto
- Apache Flink

EMR is designed for processing datasets ranging from terabytes to petabytes while automatically managing cluster provisioning and scaling.

Several deployment models were explored:

- EMR on EC2
- EMR Serverless
- EMR on EKS

Among them, **EMR Serverless** provides the simplest operational model by automatically allocating compute resources and scaling down to zero when no jobs are running.

---

# Amazon Kinesis

Next, the focus shifted to **Amazon Kinesis**, AWS's real-time data streaming platform.

## Amazon Kinesis Data Streams

Amazon Kinesis Data Streams enables continuous ingestion of streaming data from multiple producers.

Key concepts include:

- Shards
- Partition Keys
- Sequence Numbers
- Retention Period
- Consumers

Typical use cases include:

- Log aggregation
- Clickstream analytics
- IoT telemetry
- Financial transaction processing
- Real-time monitoring

Kinesis provides high-throughput, low-latency streaming for real-time analytics applications.

---

# Amazon Data Firehose

After data enters Kinesis Data Streams, **Amazon Data Firehose** automates the delivery of streaming data to storage and analytics services.

Firehose supports automatic delivery to:

- Amazon S3
- Amazon Redshift
- Amazon OpenSearch
- Splunk
- HTTP Endpoints

Important capabilities include:

- Automatic buffering
- Data compression
- Format conversion
- Lambda-based transformations
- Fully managed scaling

Unlike Kinesis Data Streams, Firehose requires no shard management, making it ideal for simple streaming delivery pipelines.

---

# AWS Lake Formation

The next topic introduced **AWS Lake Formation**, AWS's centralized data governance service.

Lake Formation simplifies the management of secure data lakes by centralizing access control across AWS analytics services.

Key features include:

- Centralized permission management
- Column-level security
- Row-level security
- Integration with AWS Glue Data Catalog
- Cross-account data sharing
- Governed Tables

Instead of maintaining multiple IAM policies and S3 bucket policies, permissions can be managed from a single governance layer.

This approach significantly reduces operational complexity in enterprise environments.

---

# Amazon Redshift

The next service explored was **Amazon Redshift**, AWS's cloud-native data warehouse.

Amazon Redshift is optimized for Online Analytical Processing (OLAP) workloads and large-scale SQL analytics.

Important concepts include:

- Columnar Storage
- Massively Parallel Processing (MPP)
- Leader Nodes
- Compute Nodes
- Redshift Spectrum
- RA3 Nodes

The learning also covered **Amazon Redshift Serverless**, which automatically provisions and scales compute resources based on workload demands.

---

## Amazon Redshift vs. Amazon Athena

A comparison between Redshift and Athena highlighted their different use cases.

| Amazon Athena | Amazon Redshift |
|---------------|-----------------|
| Queries data directly from Amazon S3 | Stores structured data in a data warehouse |
| Best for ad-hoc analytics | Best for repeated analytical workloads |
| Pay per query | Pay for compute capacity |
| No infrastructure management | High-performance analytical warehouse |

Choosing between the two depends on workload characteristics rather than one service being universally better than the other.

---

# Amazon QuickSight

The final analytics service introduced was **Amazon QuickSight**, AWS's Business Intelligence (BI) platform.

QuickSight connects directly to various AWS data sources, including:

- Amazon Athena
- Amazon Redshift
- Amazon RDS
- Amazon S3
- Amazon Aurora

Several core capabilities were explored:

- Interactive Dashboards
- SPICE In-Memory Engine
- Embedded Analytics
- ML Insights
- Natural Language Query using Amazon Q

QuickSight enables organizations to transform analytical data into interactive dashboards and business reports without maintaining separate BI infrastructure.

---

# End-to-End Analytics Workflow

After learning each individual service, the complete workflow was reviewed.

The responsibilities of each AWS service can be summarized as follows:

| Layer | AWS Service | Responsibility |
|--------|-------------|----------------|
| Ingestion | Amazon Kinesis Data Streams | Capture streaming events |
| Delivery | Amazon Data Firehose | Deliver streaming data |
| Storage | Amazon S3 | Store raw and processed data |
| Metadata | AWS Glue Data Catalog | Manage schemas and metadata |
| Governance | AWS Lake Formation | Manage permissions and data access |
| Processing | Amazon EMR | Perform large-scale data transformation |
| Analytics | Amazon Athena / Amazon Redshift | Query and analyze data |
| Visualization | Amazon QuickSight | Create dashboards and reports |

This architecture represents one of the most common patterns for building scalable analytics platforms on AWS.

---

# Key Takeaways

- Understood how AWS services integrate into a complete modern data analytics platform.
- Learned how Amazon Kinesis and Amazon Data Firehose support real-time data ingestion.
- Explored Amazon EMR for large-scale distributed data processing.
- Understood how AWS Lake Formation centralizes security and governance for data lakes.
- Compared Amazon Athena and Amazon Redshift for different analytical workloads.
- Learned how Amazon QuickSight transforms analytical results into interactive dashboards.
- Gained a comprehensive understanding of the complete AWS analytics ecosystem, from data ingestion to business intelligence.

---

*Primary Reference: https://cloudjourney.awsstudygroup.com/*