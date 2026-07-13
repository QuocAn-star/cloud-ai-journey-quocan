---
title: "Week 3 Worklog"
date: 2026-05-04
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
---

**Duration:** 04/05/2026 - 10/05/2026

## Week 3 Objectives

- Implement the Ingestion Layer for the Data Lakehouse architecture.
- Build both Batch Processing and Streaming Processing pipelines.
- Configure AWS services responsible for data ingestion.
- Validate that incoming data is successfully stored in Amazon S3.

## Tasks Completed

- Configured **Amazon API Gateway** to receive incoming requests from external applications.
- Developed **AWS Lambda** functions to process API requests and forward data into the data pipeline.
- Configured **Amazon Kinesis Data Firehose** to continuously ingest streaming events and deliver them to Amazon S3.
- Set up **Amazon EventBridge Scheduler** to automate scheduled data synchronization tasks.
- Developed Lambda functions for the **Batch Processing** pipeline to synchronize data from the source database into Amazon S3.
- Verified the functionality of both ingestion pipelines:
  - Batch Processing.
  - Streaming Processing.
- Validated that incoming data was successfully stored in the **Raw Layer** of Amazon S3.
- Monitored pipeline execution using **Amazon CloudWatch Logs** to detect errors and evaluate system performance.

## Achievements

- Successfully completed the implementation of the Data Ingestion Layer.
- Built two independent data ingestion pipelines for Batch and Streaming workloads.
- Successfully delivered incoming data into Amazon S3 through Amazon API Gateway, AWS Lambda, and Amazon Kinesis Data Firehose.
- Implemented an automated scheduling mechanism using Amazon EventBridge Scheduler for periodic data synchronization.
- Verified that the ingestion pipelines operated correctly, providing a reliable foundation for implementing the Bronze Layer ETL process in the following week.