---
title: "Week 7 Worklog"
date: 2026-06-1
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
---

**Duration:** 01/06/2026 - 07/06/2026

## Week 7 Objectives

- Configure Amazon Athena for querying analytical datasets.
- Validate the analytical tables registered in AWS Glue Data Catalog.
- Verify the accuracy of the Gold Layer datasets through SQL queries.
- Prepare the query layer for dashboard development.

## Tasks Completed

- Configured Amazon Athena to query analytical datasets stored in Amazon S3 through AWS Glue Data Catalog.
- Configured an Amazon S3 location for storing Athena query results.
- Verified all analytical tables registered in AWS Glue Data Catalog, including:
  - Dashboard Summary.
  - Daily Revenue.
  - Event Summary.
  - Country Revenue.
  - Device Summary.
  - Payment Summary.
  - Source Summary.
- Executed SQL queries to validate datasets stored in the Gold Layer.
- Compared query results with the generated analytical datasets to ensure data consistency and accuracy.
- Evaluated query performance and confirmed that Amazon Athena could efficiently query Apache Parquet datasets.
- Completed the integration between the Gold Layer and Amazon Athena to support business intelligence reporting.

## Achievements

- Successfully configured Amazon Athena together with AWS Glue Data Catalog.
- Successfully queried all analytical datasets from the Gold Layer.
- Verified that the analytical data was accurate and ready for visualization.
- Completed the Query Layer of the Data Lakehouse architecture.
- Prepared the data source for dashboard development in the following week.