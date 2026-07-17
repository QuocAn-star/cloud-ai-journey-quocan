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

| Day | Task | Date | Reference |
|:---:|------|:----:|-----------|
| **Monday** | Develop an AWS Glue ETL Job to aggregate data from the Silver Layer, perform analytical calculations, and generate datasets such as daily revenue, revenue by country, payment methods, device distribution, and other business metrics for customer behavior analysis. | 01/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |
| **Tuesday** | Store the transformed datasets in the Gold Layer on Amazon S3 using the Parquet format, then validate the structure and accuracy of the aggregated datasets before making them available for analytics. | 02/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **Wednesday** | Configure AWS Glue Data Catalog by creating a database and registering the Gold Layer tables to manage metadata and provide a centralized catalog for AWS analytics services. | 03/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html |
| **Thursday** | Verify the metadata stored in AWS Glue Data Catalog by validating table schemas, data types, and accessibility to ensure the datasets are ready for querying through Amazon Athena. | 04/06/2026 | https://docs.aws.amazon.com/glue/latest/dg/populate-data-catalog.html |
| **Friday** | Finalize the data transformation pipeline from the Silver Layer to the Gold Layer, evaluate the processing results, and prepare the analytical datasets for the Amazon Athena implementation in the following phase. | 05/06/2026 | AWS Document |


## Weekly Achievements

- Successfully completed the AWS Glue ETL pipeline from the Silver Layer to the Gold Layer.
- Built aggregated datasets for customer behavior analytics and reporting.
- Created and managed the project database and tables using AWS Glue Data Catalog.
- Prepared the Gold Layer datasets for querying through Amazon Athena.
- Completed the final layer of the Medallion Data Lakehouse architecture, enabling the analytics phase.