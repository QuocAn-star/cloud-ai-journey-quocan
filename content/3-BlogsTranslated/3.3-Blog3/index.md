---
title: "Blog 3"
date: 2026-05-25
weight: 3
chapter: false
pre: " <b> 3.3. </b> "
---

# Migrating Data and Saving Costs at Scale with Amazon S3 File Gateway

> **Original article:** [Data Migrations at Scale with Amazon S3 File Gateway](https://aws.amazon.com/vi/blogs/storage/data-migrations-at-scale-with-amazon-s3-file-gateway)

> **Translation:** [Data Migrations at Scale with Amazon S3 File Gateway](https://www.facebook.com/photo/?fbid=1029722426099971&set=gm.2200052700759690&idorvanity=660548818043427)

---

If you're managing on-premises storage servers and want to migrate a large volume of data to the cloud, you've likely encountered - or will soon face - this tricky challenge: **How do you migrate data while preserving the original file structure and creation timestamps?**

When data is "refreshed" upon upload to the cloud, you don't just lose important historical information - you also lose the opportunity to leverage automatic tiering policies to cut storage costs for aging data.

---

## 1. The Problem: Metadata Loss During Migration

When migrating data to Amazon S3 via **S3 File Gateway**, the system automatically takes the source file's **Modified Date** and assigns it as the new **Create Date** on S3.

This resets the file's age, which means **S3 Lifecycle Policies** can no longer automatically classify and push old data into cheaper storage tiers based on their true age - wasting the organization's storage budget.

---

## 2. The Solution: Automated Metadata Preservation

Instead of letting AWS reset the timestamps, you can combine **Robocopy**, **Amazon S3 File Gateway**, and **AWS Lambda** to migrate data while keeping all original metadata intact.

The Lambda function automatically reads the file's real timestamps and moves them to the appropriate storage class (like **Glacier Instant Retrieval** or **Glacier Deep Archive**) as soon as data lands on S3.

---

## 3. Why This Is the Optimal Migration Approach

| Benefit | Description |
|---------|-------------|
| **Preserve original metadata** | Retain original creation time, modification time, and NTFS access permissions during transition |
| **Cost optimization at scale** | Automatically push older files into low-cost S3 storage tiers based on their *true* age - not the cloud upload date |
| **Hybrid Cloud support** | Businesses can still access cloud data from on-premises applications via familiar SMB and NFS protocols without changing the existing environment |
| **Full automation** | Leverage Lambda's deep S3 integration to automatically execute storage class transitions - no manual intervention needed |

---

## 4. How the System Works: 3 Core Components

**Robocopy:**
Use this tool with specialized parameters (e.g., `/TIMEFIX` for timestamp sync, `/SECFIX` for permission copying) to copy data into the S3 File Gateway file share while preserving original attributes.

**Amazon S3 File Gateway:**
When automatically uploading files to S3, the gateway stores the original timestamp (`mtime`) as **user-defined metadata** attached to S3 objects.

**AWS Lambda:**
Whenever a `PUT` command writes an object to S3, Lambda is triggered, extracts the `mtime` value (in Unix time format) from the metadata, and calls the API to move the file to a low-cost storage class if it meets the age threshold.

---

## 5. Key Notes for Deployment

- **Watch Robocopy speed**: The copy process can be slow depending on file count and disk speed. Use the `/L` flag (dry run) to preview what Robocopy will do before committing to the actual copy.
- **File Gateway platform choices**: S3 File Gateway supports running as a virtual machine (VMware, Microsoft Hyper-V, Linux KVM) or as a dedicated hardware appliance at your data center.

---

## Key Takeaways

- Metadata preservation during cloud migration is not just a "nice to have" - it directly impacts storage costs
- The `mtime` field stored as S3 object metadata is the key that unlocks true-age-based lifecycle policies
- This three-component pattern (Robocopy + S3 File Gateway + Lambda) is reusable across any large-scale on-premises to cloud migration
- `/L` dry-run mode in Robocopy is your best friend before running the real migration

---

*Blog image:*

![Blog 3 - Data Migration at Scale with S3 File Gateway](/images/blog3.jpg)