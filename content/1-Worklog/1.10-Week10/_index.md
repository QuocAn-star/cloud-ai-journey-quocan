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

| Day | Task | Start Date | Completion Date | Reference |
|:---:|------|:----------:|:---------------:|-----------|
| **Monday** | - Launch an Amazon EC2 instance.<br>- Configure the Security Group, Key Pair, and networking settings.<br>- Connect to the EC2 instance via SSH. | 22/06/2026 | 22/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html |
| **Tuesday** | - Install Python and the required libraries on the EC2 instance.<br>- Upload the dashboard source code.<br>- Configure the application runtime environment. | 23/06/2026 | 23/06/2026 | https://docs.streamlit.io/deploy/tutorials |
| **Wednesday** | - Configure the connection between the dashboard and Amazon Athena.<br>- Verify data retrieval from EC2.<br>- Troubleshoot configuration issues if necessary. | 24/06/2026 | 24/06/2026 | https://aws-sdk-pandas.readthedocs.io/en/stable/ |
| **Thursday** | - Deploy the Streamlit application on Amazon EC2.<br>- Verify dashboard accessibility through the public IP address.<br>- Evaluate application performance. | 25/06/2026 | 25/06/2026 | https://docs.streamlit.io/develop/concepts |
| **Friday** | - Perform end-to-end system testing after deployment.<br>- Evaluate dashboard stability and data accessibility.<br>- Finalize the deployment environment. | 26/06/2026 | 26/06/2026 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html |

## Weekly Achievements

- Successfully deployed the analytics dashboard on Amazon EC2.
- Configured the runtime environment and integrated the application with AWS services.
- Verified that the dashboard was accessible through the public IP address and displayed analytical data correctly.
- Successfully tested the connection between Amazon EC2 and Amazon Athena.
- Completed the deployment environment, preparing the system for final testing and project completion.