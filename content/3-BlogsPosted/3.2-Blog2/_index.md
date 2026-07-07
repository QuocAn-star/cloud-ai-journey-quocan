---
title: "Blog 2"
date: 2026-01-01
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
---

# Data Governance on AWS: Ending the "Two-Place Permission" Headache for S3 and Lake Formation

> **Original article:** [Access Amazon S3 Data Files Directly Using AWS Lake Formation Permissions](https://aws.amazon.com/blogs/big-data/access-amazon-s3-data-files-directly-using-aws-lake-formation-permissions/)

> **Translation:** [Access Amazon S3 Data Files Directly Using AWS Lake Formation Permissions](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2189246758506951/?rdid=ns4Quvh0bISXoSAa#)

---

If you're a Data Scientist or ML Engineer, you've probably encountered this frustrating scenario: You have access to a data table via SQL, but when you need to read raw files from Amazon S3 to train a model, you get denied because of missing permissions in the S3 bucket policy.

Maintaining two parallel policy systems - one in Lake Formation for tables, another in IAM/S3 for files - is not only time-consuming but also carries the risk of **permission drift**.

---

## 1. The New Milestone: Unified Access Control

AWS has released an extremely valuable feature: **Directly access S3 data files using AWS Lake Formation permissions**.

Now, instead of being limited to `spark.sql()`, data scientists can directly use familiar programming functions like `spark.read.parquet()` or `spark.read.csv()` on **Amazon EMR** or **SageMaker** - while still complying with the security rules established in Lake Formation. All permissions are now managed centrally in one single place.

---

## 2. Why This Is Great News for AI and Data Projects

This feature delivers **4 core benefits** that optimize workflows:

| Benefit | Description |
|---------|-------------|
| **Unified permission system** | Query tables with Athena (SQL) and read/write S3 files with Spark (Programmatic API) - all with one set of permissions |
| **Generative AI ready** | ML pipelines can now read training data directly from governed data lakes, accelerating model development |
| **Reduced operational burden** | Operations teams no longer need to maintain complex IAM policies for each S3 bucket |
| **Easier auditing** | All access activity (both SQL and direct file access) is now recorded uniformly in AWS CloudTrail |

---

## 3. The Mechanism Under the Hood

The power of this feature lies in a new API called **`GetTemporaryDataLocationCredentials()`**, which issues temporary credentials based on the user's permissions on tables in the **AWS Glue Data Catalog**. AWS also provides a special **Java plugin** that automates permission checking and credential issuance - no manual code intervention required.

---

## 4. A Few Technical Notes for Deployment

Before getting started, keep these technical requirements in mind:

- **Permissions**: Users need `SELECT` permission on all rows and columns of a table to access the file directly.
- **Supported versions**: Requires **Amazon EMR 7.13+**, **Boto3 1.42.29+**, and **AWS CLI 2.33.1+**.
- **Format limitation**: The **Apache Iceberg** table format is not yet supported by this plugin.

---

## Key Takeaways

- One permission system to rule them all - no more dual-maintenance between Lake Formation and S3 bucket policies
- `GetTemporaryDataLocationCredentials()` is the API that makes this magic work
- A must-have for ML teams building training pipelines on governed data lakes
- Audit trail is now unified - compliance teams will appreciate this

---

*Blog image:*

![Blog 2 - Unified S3 & Lake Formation Access](/images/blog2.jpg)
