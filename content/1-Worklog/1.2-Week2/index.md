---
title: "Week 2 Worklog"
date: 2026-04-27
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

**Duration:** 27/04/2026 - 01/05/2026

## Week 2 Objectives

- Design the overall AWS Data Lakehouse architecture for the Customer Behavior Analytics project.
- Prepare the AWS environment and organize the data storage structure.
- Define the data flow for both Batch Processing and Streaming Processing pipelines.
- Plan the Medallion Architecture implementation using Bronze, Silver, and Gold layers.

## Tasks Completed

- Designed the overall architecture for the **FinOps-Optimized Serverless Medallion Data Lakehouse**.
- Identified the responsibilities of each layer in the architecture:
  - Ingestion Layer.
  - Storage Layer.
  - Processing Layer.
  - Query Layer.
  - Visualization Layer.
- Planned two data ingestion pipelines:
  - Batch Processing for scheduled database synchronization.
  - Streaming Processing for real-time customer events.
- Created the Amazon S3 bucket structure for the Medallion architecture:
  - Raw Layer.
  - Bronze Layer.
  - Silver Layer.
  - Gold Layer.
- Organized folder structures and storage conventions for analytical datasets.
- Reviewed AWS services that would be integrated into each stage of the pipeline:
  - Amazon API Gateway.
  - Amazon Kinesis Data Firehose.
  - AWS Lambda.
  - AWS Glue ETL.
  - AWS Glue Data Catalog.
  - Amazon Athena.
  - Amazon EC2.
- Prepared the development environment for implementing the ETL pipeline and dashboard in the following weeks.

## Achievements

- Completed the overall architecture design for the Customer Behavior Analytics platform.
- Defined the end-to-end data flow from data ingestion to business visualization.
- Established the Medallion storage structure on Amazon S3.
- Prepared the AWS environment and implementation plan for the ETL pipeline.
- Built a solid foundation for developing the Bronze, Silver, and Gold layers in the next phase of the project.