---
title: "Week 9 Worklog"
date: 2026-06-22
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
---

**Duration:** 22/06/2026 - 28/06/2026

## Week 9 Objectives

- Deploy the analytics dashboard to Amazon EC2 for public access.
- Configure the runtime environment for the Streamlit application.
- Connect the deployed dashboard to Amazon Athena.
- Validate the deployment process and ensure the system operates reliably.

## Tasks Completed

- Launched an Amazon EC2 instance for dashboard deployment.
- Configured the networking environment, including:
  - VPC.
  - Public Subnet.
  - Internet Gateway.
  - Route Table.
  - Security Group.
- Established SSH connectivity from the local machine to Amazon EC2 using a PEM key pair.
- Installed Python and created a virtual environment on the EC2 instance.
- Installed the required Python libraries:
  - Streamlit.
  - Pandas.
  - Plotly.
  - AWS Wrangler.
  - Boto3.
  - PyArrow.
- Configured AWS CLI and AWS credentials to enable access to AWS services.
- Connected the dashboard to Amazon Athena and AWS Glue Data Catalog.
- Resolved deployment issues, including:
  - NoRegionError.
  - NoCredentialsError.
  - Security Group configuration.
  - Public IP connectivity.
- Successfully deployed the dashboard and configured it to run continuously using `nohup`.
- Verified that the dashboard was accessible through the Amazon EC2 Public IPv4 address.

## Achievements

- Successfully deployed the analytics dashboard on Amazon EC2.
- Enabled public access to the dashboard through the EC2 Public IP.
- Established a stable connection between the dashboard, Amazon Athena, and AWS Glue Data Catalog.
- Completed the deployment environment for the Customer Behavior Analytics platform.
- Prepared the system for end-to-end integration and final validation in the following development phase.