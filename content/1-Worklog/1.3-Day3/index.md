---
title: "Day 3"
date: 2026-04-22
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
---

> **Day 3 - Infrastructure as Code and Data Engineering on AWS:** Exploring AWS CloudFormation, AWS CDK, testing infrastructure locally with Floci and LocalStack, building a simple data pipeline with AWS Glue and Amazon Athena, and deploying a relational database using Amazon RDS.

---

## Objectives

- Understand the concept of **Infrastructure as Code (IaC)** and the benefits of managing cloud infrastructure through code.
- Learn how to use **AWS CloudFormation** and **AWS CDK**.
- Test cloud infrastructure locally using **Floci** and **LocalStack**.
- Build a simple end-to-end data pipeline on AWS.
- Learn ETL workflows with **AWS Glue** and query data using **Amazon Athena**.
- Deploy and configure a relational database using **Amazon RDS**.

---

# Infrastructure as Code with AWS CloudFormation

The first topic of the day was **AWS CloudFormation**, AWS's native Infrastructure as Code (IaC) service.

Instead of manually provisioning resources through the AWS Management Console, CloudFormation allows the entire infrastructure to be described using JSON or YAML templates. This approach makes deployments repeatable, version-controlled, and consistent across environments.

A typical CloudFormation template consists of:

- Parameters
- Resources
- Outputs
- Mappings
- Conditions

Among these sections, **Resources** is the only mandatory section because it defines all AWS resources that will be created.

---

## Key Concepts

Several important CloudFormation concepts were introduced:

- **Stacks** for managing multiple AWS resources as a single deployment unit.
- **Change Sets** for previewing infrastructure changes before deployment.
- **StackSets** for deploying the same infrastructure across multiple AWS accounts or Regions.
- **Nested Stacks** for organizing large templates into reusable modules.
- **Drift Detection** for identifying manual changes made outside CloudFormation.

CloudFormation transforms infrastructure into version-controlled code that can be integrated into modern software development workflows.

---

# Infrastructure as Code with AWS CDK

After CloudFormation, the focus shifted to **AWS Cloud Development Kit (AWS CDK)**.

AWS CDK enables developers to define cloud infrastructure using familiar programming languages, including:

- TypeScript
- Python
- Java
- C#
- Go

Instead of writing CloudFormation templates manually, CDK automatically synthesizes them before deployment.

The standard deployment workflow includes:

```bash
cdk init
cdk synth
cdk deploy
cdk destroy
```

The main building blocks of AWS CDK include:

- Application
- Stack
- Constructs

Three construct levels were also introduced:

- L1 Constructs
- L2 Constructs
- L3 Constructs

AWS CDK provides several advantages, including strong type checking, IDE auto-completion, reusable infrastructure components, and improved maintainability through object-oriented programming.

---

# Testing Infrastructure with Floci and LocalStack

Once the infrastructure had been defined as code, the next step was validating it before deploying to AWS.

## Floci

Floci is a lightweight AWS emulator that allows developers to simulate AWS services locally.

Its main advantages include:

- Fast startup time
- Low memory consumption
- Local support for Amazon S3, AWS Lambda, and Amazon DynamoDB
- No AWS charges during development

Floci is especially useful for validating infrastructure and application logic during the early stages of development.

---

## LocalStack

For more comprehensive testing, **LocalStack** was introduced.

LocalStack supports a wide range of AWS services, including:

- Amazon S3
- AWS Lambda
- Amazon Kinesis
- Amazon SNS
- Amazon SQS
- Amazon DynamoDB

Running inside Docker, LocalStack enables developers to simulate a complete AWS environment on their local machines.

Local testing offers several benefits:

- Faster development cycles
- No AWS Credit consumption
- Early detection of infrastructure issues before deployment

---

# Building a Data Pipeline

With the infrastructure ready, a simple end-to-end data pipeline was designed.

The pipeline architecture follows this workflow:

```
Event Source
      ↓
Kinesis Data Streams
      ↓
Amazon Data Firehose
      ↓
Amazon S3
      ↓
AWS Glue
      ↓
Amazon Athena
      ↓
Amazon Redshift
      ↓
Amazon QuickSight
```

This pipeline demonstrates the complete lifecycle of modern data processing, from ingestion and storage to analytics and visualization.

---

# AWS Glue

The next topic covered **AWS Glue**, AWS's fully managed serverless ETL service.

The major Glue components include:

- Glue Data Catalog
- Glue Crawlers
- Glue ETL Jobs
- Glue Studio
- Glue DataBrew

AWS Glue automates several critical data engineering tasks, including:

- Schema discovery
- Metadata management
- Data transformation
- Data preparation for analytics

By automating ETL processes, Glue significantly reduces the complexity of building and maintaining data pipelines.

---

# Amazon Athena

Once data is stored in Amazon S3 and cataloged by AWS Glue, **Amazon Athena** can be used to query the data directly.

Athena is a serverless SQL query service that allows users to:

- Query data directly from Amazon S3
- Eliminate the need for database provisioning
- Avoid server management
- Pay only for the amount of data scanned

Athena supports various data formats, including:

- CSV
- JSON
- Parquet
- ORC
- Avro

Using columnar formats such as **Parquet** can significantly reduce query costs while improving performance.

---

# Deploying Amazon RDS

The final hands-on activity focused on deploying a relational database using **Amazon RDS**.

The deployment process included:

- Creating a DB Subnet Group
- Configuring Security Groups
- Launching a PostgreSQL or MySQL database
- Connecting to the database
- Cleaning up all resources after testing

During the exercise, additional concepts were explored, including:

- Deploying databases inside a VPC
- Using private subnets for database instances
- Managing automated backups
- Securing database access through Security Groups

Amazon RDS removes much of the operational burden associated with database administration by automating backups, maintenance, software updates, and infrastructure management.

---

# Key Takeaways

- Learned how to manage cloud infrastructure using Infrastructure as Code with AWS CloudFormation and AWS CDK.
- Understood how to validate AWS architectures locally using Floci and LocalStack before deploying to production.
- Built a complete data pipeline from data ingestion to analytics and visualization.
- Explored the role of AWS Glue in ETL workflows and Amazon Athena for querying data stored in Amazon S3.
- Successfully deployed a relational database using Amazon RDS while understanding the associated networking components such as VPCs, DB Subnet Groups, and Security Groups.
- Recognized how infrastructure automation and data pipelines improve development efficiency, maintainability, and deployment reliability.

---

*Primary Reference: https://cloudjourney.awsstudygroup.com/*