---
title: "Week 7 Worklog"
date: 2026-06-01
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
---

**Duration:** 01/06/2026 - 05/06/2026

## Week 7 Objectives

- Complete the data transformation process from the Silver Layer to the Gold Layer.
- Build aggregated datasets for customer behavior analytics.
- Create and manage metadata using AWS Glue Data Catalog.
- Prepare the processed data for querying with Amazon Athena.

### Tasks to Be Completed This Week

| Day | Task | Start Date | Completion Date | Reference |
|:---:|------|:----------:|:---------------:|-----------|
| **Monday** | - Design the aggregated datasets for the Gold Layer.<br>- Identify key business metrics such as revenue, payment methods, devices, and traffic sources. | 01/06/2026 | 01/06/2026 | AWS Document |
| **Tuesday** | - Develop an AWS Glue Job to transform data from the Silver Layer to the Gold Layer.<br>- Aggregate the processed data for analytics. | 02/06/2026 | 02/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/add-job.html |
| **Wednesday** | - Store the aggregated datasets in the Gold Layer on Amazon S3.<br>- Validate the accuracy and completeness of the transformed data. | 03/06/2026 | 03/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **Thursday** | - Create an AWS Glue Data Catalog database.<br>- Register the project datasets as tables in AWS Glue Data Catalog. | 04/06/2026 | 04/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html |
| **Friday** | - Verify the registered tables in AWS Glue Data Catalog.<br>- Review the data structure and prepare it for querying with Amazon Athena. | 05/06/2026 | 05/06/2026 | https://docs.aws.amazon.com/athena/latest/ug/data-sources-glue.html |

## Weekly Achievements

- Successfully completed the AWS Glue ETL pipeline from the Silver Layer to the Gold Layer.
- Built aggregated datasets for customer behavior analytics and reporting.
- Created and managed the project database and tables using AWS Glue Data Catalog.
- Prepared the Gold Layer datasets for querying through Amazon Athena.
- Completed the final layer of the Medallion Data Lakehouse architecture, enabling the analytics phase.