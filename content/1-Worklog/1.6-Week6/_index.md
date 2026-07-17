---
title: "Week 6 Worklog"
date: 2026-05-25
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
---

**Duration:** 25/05/2026 - 29/05/2026

## Week 6 Objectives
- Understand the ETL process using AWS Glue.
- Build the data transformation pipeline from the Bronze Layer to the Silver Layer.
- Perform data cleansing, standardization, and transformation.
- Prepare high-quality data for the analytics and aggregation stages.

### Tasks to Be Completed This Week

| Day | Task | Date | Reference |
|:---:|------|:----:|-----------|
| **Monday** | Study AWS Glue ETL and develop the first Glue Job to read data from the Bronze Layer stored in Amazon S3, while understanding how data is transformed between different layers in a Data Lakehouse architecture. | 25/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html |
| **Tuesday** | Perform data cleansing using AWS Glue ETL by handling missing values, standardizing column names, formatting data types, and removing invalid records to improve data quality before analytics. | 26/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html |
| **Wednesday** | Convert the processed datasets into Parquet format and store them in the Silver Layer on Amazon S3 to optimize storage efficiency and improve query performance in subsequent processing stages. | 27/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html |
| **Thursday** | Validate the transformed datasets by comparing them with the original source data, ensuring data completeness and accuracy, and confirming that the Silver Layer meets the project requirements for further aggregation. | 28/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-glue-job-cloudwatch-metrics.html |
| **Friday** | Finalize the AWS Glue ETL pipeline from the Bronze Layer to the Silver Layer, optimize the Glue Job configuration, and prepare the processed datasets for building the Gold Layer in the next phase. | 29/05/2026 | https://docs.aws.amazon.com/glue/latest/dg/populate-with-cloudformation-templates.html |


## Weekly Achievements

- Developed a solid understanding of the ETL workflow using AWS Glue.
- Successfully created an AWS Glue Job to transform data from the Bronze Layer to the Silver Layer.
- Completed data cleansing and standardization to improve data quality.
- Stored the processed dataset in the Silver Layer following the Medallion Data Lakehouse architecture.
- Successfully validated the ETL pipeline and confirmed the accuracy of the transformed data.