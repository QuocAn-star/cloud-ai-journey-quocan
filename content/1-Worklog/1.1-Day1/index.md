---
title: "Day 1"
date: 2026-04-20
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

> **Day 1 - Getting Started with AWS:** Setting up an AWS account, earning AWS Credits, establishing a cost monitoring system, and learning the fundamental concepts of Cloud Computing and core AWS services.

---

## Objectives

- Set up an AWS account and obtain AWS Credits for hands-on practice.
- Complete the introductory AWS tasks to become familiar with the AWS environment.
- Build a cost monitoring and management system from the beginning.
- Understand the fundamentals of Cloud Computing and AWS Global Infrastructure.
- Get introduced to essential AWS services such as Amazon EC2, Amazon S3, AWS IAM, AWS Lambda, and Amazon RDS.

---

# Hands-on Lab: Setting Up an AWS Account and Earning AWS Credits

To begin the First Cloud Journey program, the first step was to activate an AWS account and claim the AWS Credits provided for learners.

Initially, AWS grants **$100 in AWS Credits**. By completing five guided hands-on tasks in the AWS Console, an additional **$100 in credits** can be earned, resulting in a total of **$200 AWS Credits** for learning and experimentation.

## Task 1 - Launch an Amazon EC2 Instance

The first service explored was **Amazon EC2 (Elastic Compute Cloud)**, AWS's virtual machine service.

The hands-on activities included:

- Launching an EC2 instance.
- Creating a Key Pair.
- Configuring a Security Group.
- Launching the instance.
- Terminating the instance after completion to avoid unnecessary charges.

This exercise provided an understanding of how cloud servers are provisioned and managed within AWS.

---

## Task 2 - Amazon Bedrock Playground

The second task introduced **Amazon Bedrock**, AWS's fully managed Generative AI service.

The exercise included:

- Requesting access to Foundation Models.
- Testing the Claude 3 Haiku model.
- Running simple prompts.
- Reviewing the generated responses.

This activity demonstrated that some AI services on AWS require prior access approval as part of AWS's Responsible AI practices.

---

## Task 3 - AWS Budgets

The next task focused on configuring **AWS Budgets**.

AWS Budgets allows users to:

- Define spending limits.
- Receive email notifications when spending thresholds are reached.
- Track AWS Credit consumption.

This is one of the most important configurations when working with limited AWS Credits.

---

## Task 4 - AWS Lambda

The fourth task introduced **AWS Lambda**, AWS's serverless computing service.

The practical exercise included:

- Creating a Lambda function.
- Executing the function.
- Understanding the event-driven execution model.
- Deleting the function after testing.

This demonstrated how AWS Lambda eliminates the need to manage servers while automatically scaling based on incoming events.

---

## Task 5 - Amazon RDS

The final task involved creating a managed relational database using **Amazon RDS**.

The exercise included:

- Launching an Aurora PostgreSQL database.
- Waiting until the database became available.
- Deleting the database resources in the correct order.

This activity highlighted how Amazon RDS automates routine database administration tasks such as backups, patching, and maintenance.

---

# Building a Cost Monitoring System

After completing the initial hands-on exercises, the next step was establishing a cost monitoring strategy.

Since AWS follows a **pay-as-you-go** pricing model, monitoring resource usage from the very beginning is essential.

## AWS Budgets

Three budget thresholds were configured:

| Budget | Threshold |
|---------|-----------|
| Monthly Budget | $50 |
| Warning Budget | $25 |
| Daily Budget | $10 |

These budgets provide early warnings whenever cloud spending becomes abnormal.

---

## CloudWatch Billing Alarms

CloudWatch Billing Alarms were configured using multiple notification levels:

| Spending Threshold | Notification |
|--------------------|-------------|
| $25 | Email |
| $50 | Email + SMS |
| $75 | Email + SMS + Slack |

A multi-level alerting strategy ensures that unexpected spending can be detected as early as possible.

---

## AWS Cost Explorer

AWS Cost Explorer was enabled to:

- Monitor daily cloud costs.
- Identify the most expensive AWS services.
- Analyze AWS Credit consumption over time.

---

## Resource Tagging

All AWS resources were tagged using a consistent strategy:

| Tag | Purpose |
|-----|---------|
| Project | FCAJ |
| Environment | Dev |
| Owner | User |

Resource tagging simplifies cost allocation, resource organization, and operational management.

---

# AWS Fundamentals

After completing the hands-on labs, the focus shifted to learning the core concepts of AWS.

## Cloud Computing

Three major advantages of Cloud Computing were introduced:

- Elasticity
- Pay-as-you-go pricing
- Global Infrastructure

These principles serve as the foundation of every AWS service.

---

## AWS Global Infrastructure

The following components of AWS Global Infrastructure were studied:

- Regions
- Availability Zones (AZs)
- Edge Locations

Together, these components enable AWS to provide high availability, scalability, and low-latency services worldwide.

---

## AWS Identity and Access Management (IAM)

AWS IAM is responsible for identity and access management across AWS resources.

The following concepts were covered:

- Root Account
- IAM Users
- IAM Groups
- IAM Policies
- Multi-Factor Authentication (MFA)
- Principle of Least Privilege

IAM forms the first layer of security for every AWS environment.

---

## Overview of Core AWS Services

An introduction was provided to several fundamental AWS services:

- Amazon EC2
- Amazon S3
- Amazon RDS
- AWS Lambda

These services form the backbone of most AWS architectures and will continue to appear throughout the learning journey.

---

# Key Takeaways

- Successfully set up an AWS account and earned a total of **$200 in AWS Credits**.
- Learned how to control cloud spending using AWS Budgets, CloudWatch Billing Alarms, and AWS Cost Explorer.
- Gained a solid understanding of Cloud Computing fundamentals and AWS Global Infrastructure.
- Became familiar with essential AWS services including Amazon EC2, Amazon S3, AWS IAM, AWS Lambda, and Amazon RDS.
- Developed the habit of **cleaning up cloud resources immediately after each lab** to prevent unexpected charges.

---

*Primary Reference: https://cloudjourney.awsstudygroup.com/*