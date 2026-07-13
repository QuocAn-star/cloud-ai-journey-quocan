---
title: "Week 5 Worklog"
date: 2026-05-18
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
---

**Duration:** 18/05/2026 - 24/05/2026

## Week 5 Objectives

- Implement the Silver Layer of the Medallion Data Lakehouse architecture.
- Develop an AWS Glue ETL Job to clean and standardize data from the Bronze Layer.
- Prepare high-quality datasets for analytical processing in the Gold Layer.
- Validate data quality after the cleansing process.

## Tasks Completed

- Developed the **AWS Glue ETL Job** to transform data from the Bronze Layer into the Silver Layer.
- Removed duplicate records from all datasets.
- Standardized column names by:
  - Converting all names to lowercase.
  - Replacing spaces and hyphens with underscores.
- Trimmed unnecessary whitespace from string columns.
- Converted date and time fields into Timestamp format.
- Validated data types to ensure schema consistency across datasets.
- Stored the cleaned datasets in the Silver Layer using Apache Parquet format.
- Verified the ETL output and confirmed that the processed datasets were successfully written to Amazon S3.

## Achievements

- Successfully completed the AWS Glue ETL pipeline for the Bronze-to-Silver transformation.
- Cleaned and standardized datasets for downstream analytical processing.
- Ensured consistent schemas across all business datasets.
- Completed the implementation of the Silver Layer as the foundation for business aggregation.
- Prepared high-quality datasets for building analytical tables and KPIs in the Gold Layer.