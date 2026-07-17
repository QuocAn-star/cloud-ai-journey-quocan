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

| Day | Task | Date | Reference |
|:---:|------|:----:|-----------|
| **Monday** | Design the data storage structure on Amazon S3 based on the Data Lakehouse architecture by creating directories for Raw Data, the Bronze Layer, and Streaming Data to establish the storage environment for the project. | 18/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html |
| **Tuesday** | Implement the Batch Processing workflow by collecting customer, order, and product data from the dataset and uploading the files to Amazon S3 as the input source for the data processing pipeline. | 19/05/2026 | AWS Document |
| **Wednesday** | Study Amazon Kinesis Data Firehose and implement the Streaming Processing workflow to ingest real-time event data, while configuring Firehose to deliver streaming data directly to Amazon S3. | 20/05/2026 | https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html |
| **Thursday** | Validate the data stored in the Bronze Layer by verifying that both batch and streaming datasets were successfully delivered to Amazon S3 and checking the integrity of the ingested data before transformation. | 21/05/2026 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html |
| **Friday** | Finalize the Data Ingestion pipeline, review the storage structure, and prepare the ingested datasets for the AWS Glue ETL transformation process in the following stage. | 22/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |


## Weekly Achievements

- Successfully built the Bronze storage layer on Amazon S3.
- Organized project data following the Medallion Data Lakehouse architecture.
- Completed the Batch data ingestion process and studied Streaming Data Ingestion using Amazon Kinesis Data Firehose.
- Established the data flow from the data sources to the Bronze layer.
- Prepared the dataset for AWS Glue ETL processing in the following implementation phase.