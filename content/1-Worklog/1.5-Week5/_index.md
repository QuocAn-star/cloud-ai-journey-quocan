---
title: "Week 5 Worklog"
date: 2026-05-18
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
---

**Duration:** 18/05/2026 - 22/05/2026

## Week 5 Objectives

- Build the Bronze storage layer of the Data Lakehouse architecture.
- Prepare the Amazon S3 environment for data storage.
- Perform data ingestion from multiple data sources into the system.
- Learn the data ingestion process for both Batch Processing and Streaming Processing.

### Tasks to Be Completed This Week

| Day | Task | Start Date | Completion Date | Reference |
|:---:|------|:----------:|:---------------:|-----------|
| **Monday** | - Create an Amazon S3 bucket for the project.<br>- Design the folder structure following the Bronze, Silver, and Gold architecture. | 18/05/2026 | 18/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| **Tuesday** | - Prepare the Customer Behavior Analytics dataset.<br>- Upload batch datasets to Amazon S3.<br>- Verify the uploaded data structure. | 19/05/2026 | 19/05/2026 | https://www.kaggle.com/datasets/wafaaelhusseini/e-commerce-transactions-clickstream |
| **Wednesday** | - Study the Streaming Data Ingestion process.<br>- Learn how Amazon Kinesis Data Firehose delivers streaming data to Amazon S3. | 20/05/2026 | 20/05/2026 | https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html?utm_source=chatgpt.com |
| **Thursday** | - Design the Batch and Streaming data ingestion pipelines.<br>- Validate the data stored in the Bronze layer. | 21/05/2026 | 21/05/2026 | https://docs.aws.amazon.com/msk/latest/developerguide/integrations-redshift.html |
| **Friday** | - Evaluate the data ingestion results.<br>- Standardize the Bronze storage structure.<br>- Prepare the data for processing with AWS Glue. | 22/05/2026 | 22/05/2026 | AWS Prescriptive Guidance |

## Weekly Achievements

- Successfully built the Bronze storage layer on Amazon S3.
- Organized project data following the Medallion Data Lakehouse architecture.
- Completed the Batch data ingestion process and studied Streaming Data Ingestion using Amazon Kinesis Data Firehose.
- Established the data flow from the data sources to the Bronze layer.
- Prepared the dataset for AWS Glue ETL processing in the following implementation phase.