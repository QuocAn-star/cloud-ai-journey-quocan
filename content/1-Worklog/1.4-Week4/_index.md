---
title: "Week 4 Worklog"
date: 2026-05-11
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
---

**Duration:** 11/05/2026 - 17/05/2026

## Week 4 Objectives

- Implement the Bronze Layer of the Medallion Data Lakehouse architecture.
- Develop the first AWS Glue ETL job to transform raw data into Bronze format.
- Standardize the storage format for downstream data processing.
- Validate the quality and consistency of data stored in the Bronze Layer.

## Tasks Completed

- Developed the **Raw-to-Bronze AWS Glue ETL Job** to process raw datasets stored in Amazon S3.
- Configured the Glue job to read raw CSV files from the Raw Layer.
- Converted raw datasets into **Apache Parquet** format for optimized storage and query performance.
- Implemented schema inference to preserve data types during the transformation process.
- Organized processed datasets into separate Bronze folders for:
  - Customers.
  - Orders.
  - Products.
  - Events.
- Configured the ETL workflow to overwrite outdated data with the latest processed version.
- Verified the generated Parquet files in Amazon S3 and confirmed successful data transformation.
- Performed initial validation to ensure data completeness before proceeding to the Silver Layer.

## Achievements

- Successfully implemented the first AWS Glue ETL pipeline from Raw Layer to Bronze Layer.
- Standardized the storage format using Apache Parquet for improved analytical performance.
- Organized Bronze datasets according to the Medallion architecture.
- Verified that all source datasets were successfully transformed and stored in Amazon S3.
- Established a reliable Bronze Layer as the foundation for data cleansing and transformation in the Silver Layer.