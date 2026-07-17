---
title: "Week 10 Worklog"
date: 2026-06-15
weight: 10
chapter: false
pre: " <b> 1.10. </b> "
---

**Duration:** 22/06/2026 - 26/06/2026

## Week 10 Objectives

- Deploy the analytics dashboard to an Amazon EC2 instance.
- Configure the runtime environment and integrate the application with AWS services.
- Test external access to the deployed dashboard.
- Evaluate the system performance and stability after deployment.

### Tasks to Be Completed This Week

| Day | Task | Date | Reference |
|:---:|------|:----:|-----------|
| **Monday** | Launch an Amazon EC2 instance, configure the Key Pair, Security Group, and required networking settings, then establish an SSH connection to prepare the deployment environment for the dashboard application. | 22/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html |
| **Tuesday** | Install Python and the required libraries on Amazon EC2, upload the dashboard source code to the server, and configure the runtime environment so that the application can communicate with AWS services. | 23/06/2026 | https://docs.streamlit.io/deploy/tutorials |
| **Wednesday** | Configure the Streamlit application to connect with Amazon Athena and AWS Glue Data Catalog, verify data retrieval from EC2, and resolve configuration issues encountered during deployment. | 24/06/2026 | https://aws-sdk-pandas.readthedocs.io/en/stable/ |
| **Thursday** | Deploy the Streamlit application on Amazon EC2, configure network access, and verify that the dashboard can be accessed through the public IP address to ensure external availability. | 25/06/2026 | https://docs.streamlit.io/develop/concepts |
| **Friday** | Perform end-to-end deployment testing, evaluate dashboard performance, verify successful data retrieval from Amazon Athena, and finalize the deployment environment for the complete analytics system. | 26/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html |


## Weekly Achievements

- Successfully deployed the analytics dashboard on Amazon EC2.
- Configured the runtime environment and integrated the application with AWS services.
- Verified that the dashboard was accessible through the public IP address and displayed analytical data correctly.
- Successfully tested the connection between Amazon EC2 and Amazon Athena.
- Completed the deployment environment, preparing the system for final testing and project completion.