---
title: "Proposal"
date: 2026-05-16
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# 1. Project Overview

This project proposes the development of a **FinOps-Optimized Serverless Medallion Data Lakehouse Architecture for Customer Behavior Analytics on AWS**.

The objective of the project is to build an end-to-end data platform capable of collecting, storing, processing, querying, and visualizing customer behavior data using AWS serverless services. The architecture follows the **Medallion Data Lakehouse** approach, organizing data into Raw, Bronze, Silver, and Gold layers to improve data quality, scalability, and analytical performance.

The project demonstrates a complete Data Engineering workflow by integrating Batch Processing and Streaming Processing pipelines with AWS services such as Amazon S3, AWS Glue, Amazon Athena, AWS Glue Data Catalog, Amazon EC2, AWS Lambda, Amazon Kinesis Data Firehose, and Amazon EventBridge.

Besides building the data pipeline, the project also provides an interactive dashboard developed with Streamlit, allowing users to monitor customer behavior and business performance through real-time analytical visualizations.

---

# 2. Background

Modern organizations generate a large amount of customer behavior data from multiple sources, including online transactions, website activities, mobile applications, and user interaction events. These datasets continue to grow rapidly and often contain both structured and semi-structured information.

Traditional data warehouses are effective for structured reporting but are less flexible when handling rapidly growing datasets or multiple data sources. On the other hand, traditional data lakes provide scalable storage but often lack strong data governance and efficient analytical capabilities.

The **Data Lakehouse** architecture combines the advantages of both approaches by providing scalable storage, reliable data processing, metadata management, and high-performance analytical querying within a single platform.

To demonstrate this concept, this project develops a Customer Behavior Analytics platform on AWS. The system automatically collects customer data through Batch Processing and Streaming Processing pipelines, transforms the data using AWS Glue ETL, organizes datasets into Medallion layers, performs SQL analysis with Amazon Athena, and presents business insights through an interactive dashboard.

The project also follows **FinOps principles**, focusing on the use of serverless AWS services to reduce infrastructure management and optimize operational costs.

---

# 3. Project Objectives

## 3.1 General Objective

Develop a complete **Customer Behavior Analytics Platform** based on a **FinOps-Optimized Serverless Medallion Data Lakehouse Architecture** using AWS cloud services.

The platform should support the complete lifecycle of customer data, including ingestion, storage, transformation, analytical querying, and dashboard visualization while maintaining scalability, reliability, and cost efficiency.

## 3.2 Specific Objectives

The project aims to achieve the following objectives:

- Build Batch Processing and Streaming Processing pipelines for customer behavior data.
- Store datasets in Amazon S3 using the Medallion Architecture (Raw, Bronze, Silver, and Gold).
- Develop AWS Glue ETL Jobs to transform datasets between each Medallion layer.
- Perform data cleansing, schema standardization, and aggregation during ETL processing.
- Register analytical datasets using AWS Glue Data Catalog.
- Query business datasets through Amazon Athena.
- Develop an interactive analytics dashboard using Streamlit.
- Deploy the dashboard on Amazon EC2 for public access.
- Apply FinOps concepts by utilizing serverless AWS services and optimizing cloud resource usage.
- Build an end-to-end Data Lakehouse solution suitable for business analytics scenarios.

---

# 4. Project Scope

## 4.1 In Scope

The project includes the following components:

- Designing the overall AWS Data Lakehouse architecture.
- Building both Batch Processing and Streaming Processing pipelines.
- Implementing the Raw, Bronze, Silver, and Gold layers on Amazon S3.
- Developing AWS Glue ETL Jobs for data transformation.
- Managing metadata with AWS Glue Data Catalog.
- Performing SQL analytics using Amazon Athena.
- Developing a Streamlit dashboard for business analytics.
- Deploying the dashboard on Amazon EC2.
- Preparing technical documentation and deployment guides.

## 4.2 Out of Scope

The following items are outside the scope of this project:

- Real-time machine learning prediction or recommendation systems.
- Multi-region deployment and disaster recovery.
- Enterprise-level security implementation.
- Large-scale distributed processing using Apache Spark clusters.
- Mobile applications or customer-facing web applications.
- Production-grade monitoring and alerting systems.


# 5. Solution Architecture

The proposed solution is based on a **FinOps-Optimized Serverless Medallion Data Lakehouse Architecture** deployed on AWS.

The system is organized into five main layers:

- **Data Ingestion Layer:** Collects data from Batch Processing and Streaming Processing pipelines.
- **Storage Layer:** Stores datasets in Amazon S3 using the Medallion Architecture.
- **Processing Layer:** Performs ETL operations using AWS Glue.
- **Query Layer:** Manages metadata and executes analytical queries through AWS Glue Data Catalog and Amazon Athena.
- **Visualization Layer:** Displays business insights through a Streamlit dashboard deployed on Amazon EC2.

The overall system architecture is shown below.

![Customer Behavior Analytics Architecture](/images/2-Proposal/customer_behavior_architecture.png)

## 5.1. Data Ingestion Layer

Batch Processing workflow:

```text
Database
    │
    ▼
AWS Lambda
    │
    ▼
Amazon S3 (Raw Layer)
```

Streaming Processing workflow:

```text
Application / Event Source
        │
        ▼
Amazon Kinesis Data Firehose
        │
        ▼
Amazon S3 (Raw Layer)
```

Main activities:

1. Batch data is synchronized on a scheduled basis using Amazon EventBridge and AWS Lambda.
2. Streaming events are continuously ingested through Amazon Kinesis Data Firehose.
3. All incoming datasets are stored in the Raw Layer of Amazon S3 before further processing.

---

## 5.2. Data Processing Layer

Data transformation workflow:

```text
Raw Layer
     │
     ▼
Bronze Layer
     │
     ▼
Silver Layer
     │
     ▼
Gold Layer
```

Main activities:

1. AWS Glue ETL reads raw datasets and transforms them into the Bronze Layer.
2. The Bronze Layer stores standardized datasets while preserving the original data.
3. The Silver Layer performs data cleansing, removes duplicate records, and standardizes schemas.
4. The Gold Layer aggregates business-ready datasets for reporting and analytics.

---

## 5.3. Query and Visualization Layer

Analytics workflow:

```text
Gold Layer
      │
      ▼
AWS Glue Data Catalog
      │
      ▼
Amazon Athena
      │
      ▼
Streamlit Dashboard
      │
      ▼
Amazon EC2
```

Main activities:

1. Gold Layer datasets are registered in AWS Glue Data Catalog.
2. Amazon Athena executes SQL queries directly on datasets stored in Amazon S3.
3. The Streamlit dashboard retrieves analytical data from Amazon Athena using AWS Wrangler.
4. The dashboard is deployed on Amazon EC2, allowing users to access business analytics through a web interface.

---

# 6. AWS Services and Reasons for Selection

| AWS Service | Role in the System | Reason for Selection |
| --- | --- | --- |
| Amazon S3 | Stores Raw, Bronze, Silver, and Gold datasets | Low-cost, highly scalable, and ideal for Data Lake storage |
| AWS Glue | Performs ETL processing between Medallion layers | Fully managed serverless ETL service with seamless S3 integration |
| AWS Glue Data Catalog | Manages metadata for analytical datasets | Enables metadata management for AWS Glue and Amazon Athena |
| Amazon Athena | Executes SQL queries on analytical datasets | Serverless query service that analyzes data directly from Amazon S3 |
| AWS Lambda | Processes Batch data ingestion | Automatically executes functions without server management |
| Amazon Kinesis Data Firehose | Handles Streaming data ingestion | Continuously delivers streaming data into Amazon S3 |
| Amazon EventBridge | Schedules Batch Processing jobs | Automates periodic data synchronization |
| Amazon EC2 | Hosts the Streamlit dashboard | Provides a reliable environment for dashboard deployment |
| IAM | Controls permissions between AWS services | Ensures secure access following the least privilege principle |

---

# 7. Dataset

## 7.1. Input Data

The project uses a Customer Behavior dataset containing information such as:

- Customer Information
- Orders
- Products
- User Events
- Traffic Sources
- Payment Methods
- Countries
- Devices

The datasets are collected through both Batch Processing and Streaming Processing pipelines before entering the Data Lakehouse.

---

## 7.2. Data Processing

The datasets are processed according to the Medallion Architecture:

- **Raw Layer:** Stores the original incoming datasets.
- **Bronze Layer:** Standardizes data formats while preserving source information.
- **Silver Layer:** Cleanses, validates, and standardizes datasets.
- **Gold Layer:** Generates aggregated business datasets for analytics and reporting.

After ETL processing is completed, the Gold Layer tables are registered in AWS Glue Data Catalog and become available for querying through Amazon Athena and visualization on the Streamlit dashboard.

---

## 7.3. Output Data

The project produces several analytical datasets for business intelligence purposes, including:

- Dashboard Summary
- Daily Revenue
- Event Summary
- Country Revenue
- Device Summary
- Payment Summary
- Source Summary

These datasets provide key performance indicators (KPIs) and business insights that support customer behavior analysis and decision-making.

# 8. Implementation Roadmap

| Phase | Estimated Duration | Main Activities |
| --- | --- | --- |
| Phase 1 | Week 1 - Week 2 | Study AWS services, Data Lakehouse concepts, and design the overall architecture |
| Phase 2 | Week 3 - Week 4 | Build the Data Ingestion Layer and implement the Raw and Bronze Layers |
| Phase 3 | Week 5 - Week 6 | Develop the Silver Layer, Gold Layer, and AWS Glue ETL Jobs |
| Phase 4 | Week 7 - Week 8 | Configure AWS Glue Data Catalog, Amazon Athena, and develop the analytics dashboard |
| Phase 5 | Week 9 - Week 10 | Deploy the dashboard on Amazon EC2 and integrate the complete system |
| Phase 6 | Week 11 - Week 12 | Perform system testing, optimization, documentation, and prepare the final project report |

---

# 9. Estimated Cost

The project adopts a **serverless architecture** to minimize infrastructure management and operational costs. AWS services are charged based on actual usage, making the solution suitable for an academic project.

The primary AWS services contributing to the overall cost include:

- Amazon S3
- AWS Glue
- Amazon Athena
- Amazon EC2
- AWS Lambda
- Amazon Kinesis Data Firehose

To reduce unnecessary expenses, unused AWS resources will be stopped or removed after testing and demonstration.

---

# 10. Risks and Mitigation

| Risk | Impact | Mitigation |
| --- | --- | --- |
| AWS Glue ETL job failures | High | Monitor AWS Glue logs and validate input datasets |
| Amazon Athena query errors | Medium | Verify AWS Glue Data Catalog metadata and table schemas |
| Unexpected AWS costs | Medium | Apply FinOps practices and remove unused AWS resources |
| Dashboard cannot connect to Athena | Medium | Verify IAM permissions, AWS credentials, and AWS Region configuration |
| Dashboard deployment issues on Amazon EC2 | Low | Check Security Groups, network configuration, and Streamlit settings |

---

# 11. Expected Outcomes

Upon completion, the project is expected to achieve the following outcomes:

- Successfully build a complete AWS Data Lakehouse architecture.
- Implement both Batch Processing and Streaming Processing pipelines.
- Complete the Raw, Bronze, Silver, and Gold layers.
- Develop AWS Glue ETL Jobs for data transformation.
- Enable SQL analytics through Amazon Athena.
- Develop an interactive Streamlit analytics dashboard.
- Deploy the dashboard on Amazon EC2.
- Complete the project documentation and deployment guide.

---

# 12. Future Enhancements

The system can be extended in the future through the following improvements:

- Integrate Apache Spark for large-scale data processing.
- Expand the dashboard with additional KPIs and business analytics.
- Implement CI/CD pipelines for automated deployment.
- Integrate Machine Learning models to predict customer behavior.
- Further optimize system performance and AWS costs based on FinOps principles.
- Scale the architecture to support larger real-time data processing workloads.