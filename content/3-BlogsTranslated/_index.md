---
title: "Translated Blogs"
date: 2024-01-01
weight: 3
chapter: false
pre: " <b> 3. </b> "
---



During my internship, I translated and summarized 5 AWS technical blogs covering key topics in data engineering, cloud storage, and database management. Each blog was selected because it aligns directly with the technologies and services I worked with throughout the program.

---

### [Blog 1 - Building a Real-time CDC Pipeline: From Amazon Aurora to Amazon S3 Tables with Debezium and Firehose](3.1-Blog1/)

This blog explores how to build a real-time Change Data Capture (CDC) pipeline that moves data from Amazon Aurora PostgreSQL to Amazon S3 Tables in Apache Iceberg format. It explains why separating OLTP and OLAP workloads is critical, how Debezium on MSK Connect captures database changes with minimal performance overhead, and how AWS Lambda acts as the transformation layer that maps Debezium operation codes to Firehose insert/update/delete actions. The article also introduces how S3 Tables automates snapshot management and compaction, enabling near-real-time analytics without impacting the source database.

---

### [Blog 2 - Data Governance on AWS: Ending the "Two-Place Permission" Headache for S3 and Lake Formation](3.2-Blog2/)

This blog introduces a new AWS feature that allows data scientists and ML engineers to access raw S3 files directly using their existing AWS Lake Formation permissions - eliminating the need to maintain separate IAM/S3 bucket policies alongside Lake Formation table permissions. The article covers how the new `GetTemporaryDataLocationCredentials()` API works, how a dedicated Java plugin automates credential issuance, and why this is a game-changer for Generative AI and ML training pipelines that need governed, direct access to data lake files.

---

### [Blog 3 - Migrating Data and Saving Costs at Scale with Amazon S3 File Gateway](3.3-Blog3/)

This blog addresses a common but often overlooked problem in cloud migrations: when files are moved from on-premises storage to Amazon S3 via S3 File Gateway, their original creation timestamps get reset - which breaks S3 Lifecycle Policies that depend on file age. The article presents an automated solution combining Robocopy, S3 File Gateway, and AWS Lambda to preserve original file metadata (timestamps, NTFS permissions) and automatically route files into the correct low-cost storage class (e.g., Glacier Deep Archive) based on their true age - optimizing storage costs at scale while supporting hybrid cloud access via SMB and NFS.

---

### [Blog 4 - Automating Amazon Aurora PostgreSQL Upgrades: Reducing DBA Workload by 80%](3.4-Blog4/)

This blog presents a comprehensive automation framework for managing major and minor version upgrades across a fleet of Amazon Aurora PostgreSQL clusters. Using AWS Systems Manager as the orchestrator and Amazon EC2 for script execution, the solution reduces manual upgrade effort by up to 80%. Key highlights include a tag-based activation mechanism (`UpgradeDB: Y`), Aurora Copy-on-Write cloning for zero-risk pre-upgrade validation, a two-phase process (PREUPGRADE checks + actual UPGRADE), and centralized logging to S3 with SNS notifications - giving DBAs full visibility and a safety net without the toil.

---

### [Blog 5 - Introducing Amazon S3 Object Lambda: Ending the "Data Duplication" Problem When Retrieving from S3](3.5-Blog5/)

This blog introduces Amazon S3 Object Lambda, a feature that lets you add custom processing code that runs inline whenever an application retrieves data from S3 - before the data is returned. Instead of maintaining multiple copies of the same dataset for different consumers (masked for analytics, enriched for marketing, reformatted for another service), a single Lambda function handles the transformation on-demand. The article covers the `inputS3Url` pattern that decouples Lambda from direct S3 permissions, the `WriteGetObjectResponse` API for streaming large objects, and key use cases including PII masking, format conversion, and dynamic data generation.
