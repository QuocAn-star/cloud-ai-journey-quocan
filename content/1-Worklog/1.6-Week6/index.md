---
title: "Week 6 Worklog"
date: 2026-05-25
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
---

**Duration:** 25/05/2026 - 31/05/2026

## Week 6 Objectives

- Implement the Gold Layer of the Medallion Data Lakehouse architecture.
- Develop an AWS Glue ETL Job to generate analytical datasets.
- Build business-oriented analytical tables for dashboard visualization.
- Register Gold Layer tables in AWS Glue Data Catalog for Amazon Athena queries.

## Tasks Completed

- Developed the **AWS Glue ETL Job** to transform data from the Silver Layer into the Gold Layer.
- Created analytical datasets including:
  - Dashboard Summary.
  - Daily Revenue.
  - Event Summary.
  - Country Revenue.
  - Device Summary.
  - Payment Summary.
  - Source Summary.
- Implemented aggregation logic to calculate:
  - Total orders.
  - Total customers.
  - Total revenue.
  - Average order value.
  - Revenue grouped by country, device, payment method, and traffic source.
- Stored all analytical datasets in the Gold Layer using Apache Parquet format.
- Automatically registered the Gold tables in **AWS Glue Data Catalog**.
- Verified the schema and confirmed successful table registration in the Glue Catalog.

## Achievements

- Successfully completed the AWS Glue ETL pipeline for the Silver-to-Gold transformation.
- Built multiple analytical datasets to support business intelligence reporting.
- Completed the implementation of the Gold Layer following the Medallion architecture.
- Successfully registered analytical tables in AWS Glue Data Catalog.
- Prepared the datasets for querying with Amazon Athena and dashboard visualization in the next development phase.