---
title: "Day 2"
date: 2026-04-21
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

> **Day 2 - Compute, Networking, and Storage on AWS:** Exploring AWS CLI, Amazon EC2, Amazon VPC, Amazon CloudFront, AWS Lambda, AWS CDK, and storage management with Amazon S3.

---

## Objectives

- Learn how to manage AWS resources using the AWS Command Line Interface (CLI).
- Understand the fundamentals of Amazon VPC and networking on AWS.
- Deploy a web server on Amazon EC2 inside a custom VPC.
- Explore content delivery with Amazon CloudFront and edge computing using Lambda@Edge.
- Understand the serverless execution model of AWS Lambda.
- Learn Infrastructure as Code using AWS CDK.
- Configure Amazon S3 Lifecycle Policies and automate Amazon EBS snapshot management.

---

# AWS Command Line Interface (AWS CLI)

The day began by learning **AWS CLI**, the unified command-line tool for interacting with AWS services.

Instead of managing resources through the AWS Console, AWS CLI allows infrastructure to be created, queried, and automated directly from the terminal.

Key concepts included:

- Installing and configuring AWS CLI using `aws configure`.
- Managing AWS credentials and named profiles.
- Executing common commands such as:
  - `aws s3 ls`
  - `aws ec2 describe-instances`
  - `aws iam list-users`
- Filtering results using **JMESPath** with the `--query` option.
- Formatting outputs using JSON, Table, and Text.

AWS CLI serves as the foundation for automation and DevOps workflows throughout the AWS ecosystem.

---

# Deploying a Web Server on Amazon EC2

The primary hands-on activity was deploying a complete web server inside a custom Virtual Private Cloud.

## Building a Custom Amazon VPC

Instead of using the default VPC, a custom networking environment was created from scratch.

The architecture included:

- One Virtual Private Cloud (VPC)
- One Public Subnet
- Internet Gateway
- Route Table
- Security Group

This exercise demonstrated how AWS networking components work together to provide internet connectivity.

---

## Launching an Amazon EC2 Instance

After the networking infrastructure was ready, an Amazon EC2 instance was launched.

The configuration included:

- Amazon Linux AMI
- t2.micro instance
- Public subnet placement
- HTTP and SSH security rules

A User Data script was also configured to automatically install Apache Web Server during the first boot.

After deployment, the web application became accessible through the instance's public IP address.

This exercise provided a complete understanding of how applications are hosted on AWS.

---

# Amazon CloudFront and Lambda@Edge

Next, the focus shifted toward global content delivery.

## Amazon CloudFront

Amazon CloudFront is AWS's Content Delivery Network (CDN) that caches content at edge locations around the world.

Major concepts covered included:

- CloudFront Distributions
- Origins
- Behaviors
- Cache Policies
- HTTPS enforcement
- Edge Locations

CloudFront significantly reduces latency by serving content from locations closest to end users.

---

## Lambda@Edge

Lambda@Edge extends AWS Lambda to CloudFront edge locations.

Common use cases include:

- URL rewriting
- Authentication
- Header manipulation
- Image optimization
- A/B testing

Running code closer to users reduces latency without modifying backend services.

---

# AWS Lambda

The next topic introduced **AWS Lambda**, AWS's serverless computing platform.

Instead of provisioning servers, developers simply upload code while AWS automatically manages:

- Infrastructure
- Scaling
- Availability
- Operating system maintenance

Important concepts included:

- Event-driven architecture
- Lambda Functions
- Handlers
- Triggers
- Concurrency
- Lambda Layers
- Environment Variables
- Lambda Function URLs

The pricing model is based entirely on the number of requests and execution duration, making Lambda highly cost-efficient for event-driven workloads.

---

# Infrastructure as Code with AWS CDK

After understanding serverless computing, the learning continued with **AWS Cloud Development Kit (CDK)**.

AWS CDK enables developers to define infrastructure using familiar programming languages instead of manually creating CloudFormation templates.

Core concepts included:

- Constructs
- Stacks
- Applications
- L1, L2, and L3 Constructs

The standard deployment workflow consists of:

```bash
cdk init
cdk synth
cdk deploy
cdk destroy
```

Compared with writing raw CloudFormation templates, CDK offers:

- Type safety
- IDE auto-completion
- Reusable components
- Better code organization

Infrastructure can therefore be managed using the same software engineering practices applied to application development.

---

# AWS Toolkit for Visual Studio Code

To improve the development experience, AWS Toolkit for VS Code was introduced.

The toolkit provides direct access to AWS services without leaving the IDE.

Features explored included:

- Browsing Lambda functions
- Viewing CloudWatch Logs
- Managing Amazon S3 objects
- Running and debugging Lambda functions locally
- Managing AWS credentials and profiles

This significantly shortens the development and testing cycle.

---

# Amazon S3 Lifecycle Policies

Storage optimization was another important topic of the day.

Amazon S3 Lifecycle Policies automate storage management by moving objects between storage classes based on predefined rules.

Example lifecycle configuration:

| Action | Time |
|---------|------|
| Transition to S3 Standard-IA | After 30 days |
| Transition to Glacier Instant Retrieval | After 90 days |
| Delete expired objects | After 365 days |

Lifecycle Policies help reduce storage costs without requiring manual intervention.

---

# Amazon EBS Data Lifecycle Manager

The final topic covered **Amazon EBS Data Lifecycle Manager (DLM)**.

Instead of manually creating snapshots, DLM automates:

- Snapshot scheduling
- Retention policies
- Cross-region snapshot replication
- Backup lifecycle management

Automating snapshots ensures that backup strategies remain consistent while minimizing operational effort.

---

# Key Takeaways

- Learned how to automate AWS operations using AWS CLI.
- Built a complete networking environment with Amazon VPC and deployed an EC2 web server.
- Understood how Amazon CloudFront accelerates global content delivery and how Lambda@Edge executes code closer to end users.
- Explored AWS Lambda as the foundation of serverless architectures.
- Learned Infrastructure as Code using AWS CDK and integrated AWS Toolkit into the development workflow.
- Configured Amazon S3 Lifecycle Policies to optimize storage costs.
- Automated backup management using Amazon EBS Data Lifecycle Manager.

---

*Primary Reference: https://cloudjourney.awsstudygroup.com/*