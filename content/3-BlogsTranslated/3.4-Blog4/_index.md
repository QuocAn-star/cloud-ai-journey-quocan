---
title: "Blog 4"
date: 2026-01-01
weight: 4
chapter: false
pre: " <b> 3.4. </b> "
---

# Automating Amazon Aurora PostgreSQL Upgrades: Reducing DBA Workload by 80%

> **Original article:** [Automate Amazon Aurora PostgreSQL Major or Minor Version Upgrade Using AWS Systems Manager and Amazon EC2](https://aws.amazon.com/blogs/database/automate-amazon-aurora-postgresql-major-or-minor-version-upgrade-using-aws-systems-manager-and-amazon-ec2/)

> **Author:** Rajeev Pardipuram, Anand Komandooru, Sameer Kumar, and Li Liu

> **Translation:** [Automate Amazon Aurora PostgreSQL Major or Minor Version Upgrade Using AWS Systems Manager and Amazon EC2](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2181404265957867/?rdid=g9DRm6bfvHIxjqpG#)


---

Managing and upgrading major or minor versions across a fleet of Amazon Aurora PostgreSQL clusters has never been easy. Done manually, it not only takes hours but also carries a high risk of configuration errors.

This article shares a **comprehensive automation solution** that optimizes this process through the combination of **AWS Systems Manager** and **Amazon EC2**.

---

## 1. Why Should You Care About This Solution?

The standout feature of this solution is its ability to **reduce manual effort by up to 80%**. Instead of logging into each cluster individually, you can now orchestrate upgrades across your entire database fleet consistently and safely.

Critically, the solution leverages **Aurora's Copy-on-Write cloning** feature. Before making any changes to real data, the system creates an ultra-fast clone - ensuring you always have a safety net if something goes wrong.

---

## 2. The Automation Framework

This is not just a single script - it's a closed-loop process using core AWS services:

| Service | Role |
|---------|------|
| **AWS Systems Manager** | The "conductor" - orchestrates all work |
| **Amazon EC2** | Executes automation scripts and CLI commands |
| **AWS Secrets Manager** | Securely stores DB admin passwords |
| **Amazon S3** | Stores detailed logs from each upgrade run |
| **Amazon SNS** | Sends email notifications when the process completes |

---

## 3. The Two-Phase Upgrade Process

The system uses **tags** as the activation mechanism - you simply tag clusters with `"UpgradeDB: Y"` and the system automatically identifies them. The process runs in two phases:

### Phase 1: PREUPGRADE (Pre-upgrade Validation)
This is a critically important step. The system will:
- Check the status of replication slots
- Perform `VACUUM` tasks
- Generate a readiness report: Is this DB ready to be upgraded?

### Phase 2: UPGRADE (Actual Upgrade)
Once everything is validated, activate this mode for the system to:
- Perform the engine version upgrade
- Update extensions
- Run `ANALYZE` to optimize performance immediately after upgrading

---

## 4. Excellent Monitoring Capabilities

One of the best aspects of this solution is its **detailed logging system**. Every action - from creating the clone, backing up the configuration, to the result of each extension update - is recorded and pushed to S3.

If one cluster encounters an error, you'll know exactly where the problem lies and can fix it **without affecting other clusters**.

---

## 5. Closing Thoughts

If you're managing a large data system on AWS, moving from manual upgrades to automation is an inevitable step. It not only helps you "sleep better" during every maintenance window but also ensures maximum stability for your application.

Start by testing this in a non-production environment and gradually roll it out - the time investment upfront will pay dividends in reliability and peace of mind.

---

## Key Takeaways

- The tag-based activation (`UpgradeDB: Y`) is elegantly simple and scalable
- Copy-on-Write cloning provides a safety net with virtually zero performance impact
- Two-phase design (PREUPGRADE → UPGRADE) prevents surprise failures during actual upgrades
- Centralized logging in S3 means you can audit every action across your entire fleet

---

*Blog image:*

![Blog 4 - Automating Aurora PostgreSQL Upgrades](/images/blog4.jpg)