---
title: "Proposal"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# FinOps-Optimized Serverless Medallion Data Lakehouse Architecture for Customer Behavior Analytics

---

## 1. Project Overview

This proposal presents the design and end-to-end implementation of a **cloud-native, fully serverless data lakehouse** on AWS - purpose-built to analyze customer behavior in an e-commerce context. The platform is named **"FinOps-Optimized Serverless Medallion Data Lakehouse"** to reflect two foundational design principles baked into every architectural decision:

1. **FinOps-first (Cost optimization as the top priority)**: Every AWS service choice is selected to minimize cost - serverless compute (zero idle cost), on-demand queries, in-flight data transformation that eliminates intermediate storage writes, and intelligent S3 storage tiering. The platform delivers production-grade analytics capability at a total estimated cost under **$8/month** at internship-scale workloads.

2. **Medallion Architecture**: Raw data flows through three progressively refined S3 tiers - **Bronze** (raw, immutable landing zone) → **Silver** (cleansed, schema-validated) → **Gold** (business-aggregated, analytics-ready) - ensuring that data quality improves at every stage while preserving the ability to replay the entire pipeline from raw data at any time.

The platform unifies **two ingestion paths**: real-time clickstream events from web and mobile applications (streaming path via API Gateway → Firehose) and periodic order records from a transactional database (batch path via EventBridge → Lambda). Both paths land in the same S3 Bronze bucket, ensuring a single source of truth regardless of data origin. Downstream, AWS Glue ETL jobs transform data through the Medallion tiers, Amazon Athena provides serverless SQL analytics, and a **Streamlit Dashboard** surfaces business-ready KPIs to stakeholders.

> **Overall Architecture Diagram:**

![FinOps-Optimized Serverless Medallion Data Lakehouse Architecture](/images/2-Proposal/de.png)

**Platform at a glance:**

| Dimension | Detail |
|-----------|--------|
| **Use case** | E-commerce customer behavior analytics |
| **Ingestion** | Real-time streaming (clickstream) + scheduled batch (orders) |
| **Storage pattern** | Medallion Architecture: Bronze → Silver → Gold on Amazon S3 |
| **Processing** | AWS Glue ETL (PySpark) - serverless, pay-per-DPU-second |
| **Analytics** | Amazon Athena - serverless SQL, pay-per-TB-scanned |
| **Visualization** | Python Streamlit Dashboard via PyAthena |
| **IaC** | AWS CDK (TypeScript) - entire platform defined as code |
| **Estimated monthly cost** | ~$7–8/month at internship scale |
| **Governance** | IAM least-privilege + KMS CMKs + CloudWatch observability |

---

## 2. Objectives

The platform is designed to achieve the following measurable objectives:

### 2.1. Technical Objectives

**O1 - Dual-path unified ingestion:**
Build and validate two distinct data ingestion paths that both land into a single S3 Bronze bucket:
- Streaming path: real-time clickstream events from web/mobile → API Gateway → Firehose + Lambda → S3 Bronze, with sub-second edge validation and in-flight transformation.
- Batch path: transactional order records → EventBridge Scheduler → Lambda DB extractor (watermark-based) → S3 Bronze, on a configurable hourly/daily cadence.

**O2 - Three-tier Medallion data quality pipeline:**
Implement two sequential AWS Glue ETL jobs that progressively refine data quality:
- **Glue ETL Job 1 (Bronze → Silver)**: deduplication, null handling, schema enforcement, type casting, Parquet conversion with Snappy compression.
- **Glue ETL Job 2 (Silver → Gold)**: business KPI aggregations - daily revenue by category, user funnel conversion rates, customer LTV segmentation, product performance metrics.

**O3 - Serverless SQL analytics with FinOps optimization:**
Configure Amazon Athena with a dedicated Workgroup that enforces per-query data scan limits, combined with Parquet columnar format and Hive-style partitioning to reduce effective data scanned by 85–90% compared to raw JSON - delivering sub-second query performance on Gold-tier data at minimal cost.

**O4 - Interactive Streamlit Dashboard:**
Develop a Python Streamlit web application connected to Athena via `pyathena` that renders at least 5 business KPI visualizations (sales funnel, revenue trends, product leaderboard, customer cohort analysis, real-time event feed) with 5-minute result caching to minimize repeat query costs.

**O5 - Infrastructure as Code (IaC):**
Define the entire platform - S3 buckets, IAM roles, KMS keys, Glue resources, API Gateway, Lambda, Firehose, EventBridge, Athena Workgroup - as AWS CDK TypeScript constructs, enabling repeatable one-command deployment (`cdk deploy`) and teardown (`cdk destroy`).

**O6 - Governance and observability:**
Implement least-privilege IAM roles per service, AWS KMS Customer Managed Keys per S3 tier, and a CloudWatch Dashboard with alarms covering Lambda error rates, Glue Job failures, Firehose throttling, and Athena query timeouts.

### 2.2. Learning Objectives

Beyond the technical deliverables, this project serves as a hands-on internship learning experience to develop proficiency in:

| Skill Area | AWS Services / Tools |
|------------|---------------------|
| Serverless compute | AWS Lambda, Amazon API Gateway |
| Streaming ingestion | Amazon Data Firehose |
| Batch orchestration | Amazon EventBridge Scheduler |
| Data lake storage | Amazon S3, Parquet, Snappy compression |
| ETL & data engineering | AWS Glue PySpark, Glue Data Catalog |
| SQL analytics | Amazon Athena, query optimization |
| Security & governance | AWS IAM, AWS KMS, CloudTrail |
| Infrastructure as Code | AWS CDK (TypeScript) |
| Data visualization | Python Streamlit, PyAthena, Pandas |
| FinOps / cost optimization | S3 lifecycle, Athena Workgroup, Parquet columnar format |

---

## 3. Problem Statement

### 3.1. Business Context

Modern e-commerce businesses generate enormous volumes of data every second - from real-time user clickstream events on websites and mobile applications (page views, product clicks, add-to-cart, checkout completions) to transactional order records stored in backend relational databases. When properly harnessed, this data unlocks powerful insights into customer behavior patterns, sales funnel conversion rates, product performance, and operational efficiency.

However, for small-to-medium e-commerce teams (and internship-scale projects operating on limited AWS credits), accessing these insights is blocked by a set of interconnected infrastructure challenges:

### 3.2. Five Core Problems

**Problem 1 - Dual data velocity with no unified landing zone**

Clickstream events arrive continuously at variable rates (0 to thousands of events per second), requiring low-latency, high-throughput streaming ingestion. Order records, by contrast, are produced by a transactional OLTP database that cannot be queried continuously without degrading production performance - requiring a scheduled batch extraction pattern.

Without a platform that handles both, teams are forced to choose: build two separate pipelines with separate storage, or collapse everything into a batch process that discards the real-time behavioral signal entirely.

**Problem 2 - Data quality degradation with no enforcement layer**

Client-generated event payloads are inherently unreliable: they may contain malformed JSON, missing required fields, invalid data types, duplicate event IDs (from client retry logic), or stale timestamps. Without a validation and transformation layer, these defects propagate silently into downstream analytics - corrupting KPIs, inflating user counts, and generating misleading business decisions.

**Problem 3 - Cost vs. scale tension with traditional approaches**

Traditional analytics solutions for this use case (e.g., an always-on Redshift cluster, a perpetually running EMR cluster, or a persistent Kafka broker) incur significant fixed costs regardless of actual query or processing volume. For a project with a finite AWS credit budget and highly variable workloads (low overnight, high during business hours), this fixed-cost model is economically unsustainable.

| Traditional Approach | Monthly Cost Estimate | Problem |
|----------------------|-----------------------|---------|
| Amazon Redshift (ra3.xlplus, 2 nodes) | ~$700–900/month | Massive over-provisioning for internship scale |
| Amazon EMR (m5.xlarge, 3 nodes) | ~$300–500/month | Cluster idle cost between batch runs |
| Amazon MSK (kafka.m5.large, 3 brokers) | ~$400–600/month | 24/7 cost even when no events are flowing |
| **This platform (fully serverless)** | **~$7–8/month** | **Pay only for actual usage** |

**Problem 4 - No centralized governance or access control**

Without a structured platform, data engineers tend to apply S3 bucket policies and IAM permissions ad-hoc - leading to "permission sprawl" where services accumulate more access than they need. Sensitive customer data (email addresses, purchase histories, behavioral profiles) becomes accessible to any team member or service with an S3 read permission, violating least-privilege principles and creating compliance exposure.

**Problem 5 - No schema management or query optimization**

Raw JSON data stored in S3 has no associated schema catalog, making it impossible for SQL tools like Athena to understand table structures without a manual `CREATE TABLE` statement. Additionally, querying raw JSON with Athena is dramatically more expensive than querying Parquet (Athena charges per TB scanned - JSON files are 5–10x larger than equivalent Parquet files for the same logical data).

### 3.3. Why This Matters

Without solving these five problems, the e-commerce analytics capability remains either:
- **Non-existent** (no platform built) - business decisions made on intuition, not data
- **Fragile** (ad-hoc scripts, manual SQL) - not reproducible, not scalable, not governed
- **Expensive** (always-on clusters) - not sustainable on internship-scale AWS credits

This proposal solves all five problems simultaneously through a cohesive, serverless, IaC-defined data lakehouse that is both cost-efficient and production-ready.

---

## 4. Solution Architecture

### 4.1. Architecture Overview

The platform is organized into **six functional layers** plus a **horizontal governance layer**, each with precisely defined responsibilities:

| Layer | AWS Services | Responsibility |
|-------|-------------|---------------|
| **Data Source** | Website, Mobile App, E-commerce Orders DB | Event generation and transactional records |
| **Ingestion Layer** | API Gateway, Data Firehose, Lambda, EventBridge Scheduler | Dual-path data capture and edge validation |
| **Storage Layer** | Amazon S3 (Bronze / Silver / Gold) | Medallion-tier immutable data lake storage |
| **Processing Layer** | AWS Glue ETL Jobs, Glue Data Catalog | Schema transformation and business aggregation |
| **Query Layer** | Amazon Athena, Glue Data Catalog | Serverless SQL analytics over S3 |
| **Visualization Layer** | Streamlit Dashboard | Interactive business KPI exploration |
| **Governance** | AWS IAM, AWS KMS, Amazon CloudWatch | Security, encryption, and observability |

---

### 4.2. Data Sources

**Source 1 - Website & Mobile Application (Real-Time Events)**

User-facing web and mobile applications emit behavioral events continuously - page views, product detail views, add-to-cart, checkout initiations, purchase completions, and session terminations. Each event is a structured JSON payload sent via HTTP POST to the ingestion endpoint. Volume is highly variable: near-zero at 3 AM, peaking during flash sales.

- **Format**: JSON, schema-versioned per event type
- **Velocity**: 0 to thousands of events/second (unpredictable)
- **Latency requirement**: Sub-second ingestion; analytics acceptable within minutes
- **Quality risk**: Malformed JSON, missing required fields, invalid types from client bugs

**Source 2 - E-commerce Orders Database (Batch Records)**

A transactional relational database (PostgreSQL/MySQL) stores completed order records including order ID, customer ID, SKUs, quantities, prices, payment status, and fulfillment timestamps. Cannot be queried continuously without degrading OLTP performance.

- **Format**: Relational rows → extracted as Apache Parquet
- **Velocity**: Batch, extracted hourly or daily
- **Latency requirement**: T+1 hour acceptable
- **Quality risk**: Duplicate records from retry logic; partial updates from long-running transactions

---

### 4.3. Ingestion Layer

**Path A - Web / Mobile Streaming** *(Steps 1 → 2 → 3)*

**Step 1 - Amazon API Gateway: Edge Ingestion & Validation**

All client events enter through an HTTP POST endpoint on **Amazon API Gateway** (REST API). A **Request Validator** enforces a strict **JSON Schema** at the edge - malformed requests are rejected immediately with `400 Bad Request` before reaching any downstream service.

> **FinOps impact**: Validation at API Gateway costs nothing extra - bad data is rejected before Lambda or Firehose is ever invoked, preventing wasteful downstream compute.

**Step 2 - Amazon Data Firehose + AWS Lambda: Buffering & Inline Transformation**

Validated payloads flow into an **Amazon Data Firehose** delivery stream. Firehose is chosen over Kinesis Data Streams because it requires zero shard capacity planning, natively buffers and batches records before S3 delivery, and supports synchronous inline Lambda invocations.

Firehose synchronously invokes a lightweight **AWS Lambda** function (128 MB RAM) for in-flight transformation:
- Normalize event timestamps to UTC ISO-8601
- Enrich records with pipeline metadata
- Soft-validate secondary fields (flag anomalies without dropping records)
- Return transformed records **in memory** - no intermediate S3 write made

> **FinOps impact**: In-RAM Lambda transformation eliminates the intermediate S3 PUT+GET cycle that traditional "write-then-read" transformation pipelines incur.

**Step 3 - S3 Bronze Bucket: Streaming Sink**

Firehose flushes buffered records as **NDJSON**, partitioned by:
```
s3://[project]-bronze/events/year=YYYY/month=MM/day=DD/hour=HH/
```

The Bronze bucket is **raw and immutable** - data is preserved exactly as received, serving as the single source of truth for full pipeline reprocessing.

---

**Path B - DB Sync / Batch** *(Step 8 → Lambda → S3 Bronze)*

**Step 8 - Amazon EventBridge Scheduler: Orchestration Trigger**

An **EventBridge Scheduler** rule fires on a cron expression (e.g., `rate(1 hour)`). Zero always-on infrastructure - no EC2, no container, no persistent process. Cost incurred only during execution window.

**AWS Lambda - DB Extractor Function**

The trigger invokes a **Lambda function** that:
1. Retrieves DB credentials from **AWS Secrets Manager** (never hardcoded)
2. Queries records using a **watermark pattern**: `WHERE updated_at > last_successful_run_timestamp`
3. Converts result set to **Apache Parquet** in memory using PyArrow
4. Writes Parquet files to S3 Bronze under a logically separate prefix:
```
s3://[project]-bronze/orders/year=YYYY/month=MM/day=DD/batch_id=UUID/
```
5. Persists the new watermark timestamp to **AWS SSM Parameter Store** for idempotent re-runs

---

### 4.4. Storage Layer - Medallion Architecture

The platform implements the **Medallion Architecture** - each S3 tier represents a progressively higher level of data quality and business readiness:

| Tier | S3 Bucket | Format | Partition Key | Description |
|------|-----------|--------|---------------|-------------|
| **Bronze** | `[proj]-bronze` | NDJSON (stream) / Parquet (batch) | `year/month/day/hour` | Raw, immutable. Full reprocessing always possible from here. |
| **Silver** | `[proj]-silver` | Parquet + Snappy | `year/month/day` | Cleansed, deduplicated, schema-validated. Optimized for query. |
| **Gold** | `[proj]-gold` | Parquet + Snappy | `metric_date/category` | Pre-aggregated KPIs. Directly consumed by visualization layer. |

**Why Parquet + Snappy?**
- Up to **87% storage reduction** vs. raw JSON → lower S3 storage cost
- **Column pruning**: Athena reads only accessed columns → less data scanned → lower query cost
- **Predicate pushdown**: Athena skips entire row groups that don't match WHERE filters → faster and cheaper queries

**Example Gold datasets produced:**
- `daily_revenue_by_category` - revenue per product category per day
- `user_funnel_daily` - user counts at each funnel stage (view → cart → checkout → purchase)
- `customer_ltv_segments` - 90-day cumulative order value bucketed into LTV tiers
- `product_performance_weekly` - view-to-purchase conversion rate per product, trailing 7 days

**Security:** All three buckets encrypted at rest using **AWS KMS Customer Managed Keys (CMKs)** - one CMK per tier. S3 bucket policies enforce zero cross-tier write access.

---

### 4.5. Processing Layer - AWS Glue ETL Pipeline

**Glue ETL Job 1 - Bronze → Silver Transformation (Step 5)**

Triggered by EventBridge after batch ingestion completes. Reads from Bronze, applies:
1. **Schema enforcement** - cast fields to canonical data types
2. **Deduplication** - window function on `event_id` / `order_id`, keeping most recent
3. **Null handling** - fill optional nulls with defaults; quarantine records with missing required fields to `_quarantine/` prefix
4. **String normalization** - lowercase categories, standardize phone/email formats
5. **Format conversion** - output Parquet + Snappy, partitioned by `year/month/day`

On completion: calls Glue Data Catalog API to register new Silver partitions - **no Crawler needed**.

**Glue ETL Job 2 - Silver → Gold Aggregation (Step 6)**

Runs after Job 1. Reads from Silver, computes:
1. Revenue aggregation: `SUM(order_total) GROUP BY (category, order_date)`
2. Funnel analysis: distinct user counts per `event_type` per day + stage conversion rates
3. Customer LTV segmentation: 90-day cumulative spend per `customer_id` → LTV bucket labels
4. Product performance: view-to-purchase rate per `product_id` over trailing 7-day windows
5. Session reconstruction: group clickstream events into sessions (30-min inactivity gap) → compute session duration and pages-per-session

On completion: registers Gold table partitions in Glue Data Catalog.

**Glue Data Catalog (Step 7)**

Central metadata registry for all three tiers. Stores table schemas, partition keys, and S3 physical locations. Both ETL jobs register output directly via Catalog API - **no periodic Crawlers**, eliminating scheduled DPU-hour crawl costs. Amazon Athena reads from the Catalog to plan optimized query execution without data movement.

---

### 4.6. Query Layer - Amazon Athena

Amazon Athena provides **serverless, interactive SQL analytics** directly over S3 - no cluster, no provisioning, pay only per TB scanned.

**FinOps optimization stack for Athena:**

| Optimization | Mechanism | Cost Impact |
|-------------|-----------|------------|
| Parquet columnar format | Silver + Gold stored as Parquet | 70–90% data scan reduction vs. JSON |
| Snappy compression | All Parquet files compressed | Smaller S3 objects → less data transferred |
| Hive partitioning | `year/month/day` partition keys | Athena prunes irrelevant partitions before scanning |
| Pre-aggregated Gold tier | Dashboard queries hit Gold, not Silver | Scan thousands of rows vs. millions of raw events |
| Query result reuse | Athena result caching enabled | Identical queries within 24h return cached results at $0 |
| Workgroup scan limit | Per-query data limit set (e.g., 1 GB max) | Prevents runaway queries from draining AWS credits |

Athena is accessed programmatically by Streamlit via `pyathena` (DBAPI2 interface) with parameterized SQL. Results stored in a dedicated S3 results bucket for audit trails and caching.

---

### 4.7. Visualization Layer - Streamlit Dashboard

A **Python Streamlit web application** connects to Athena via `pyathena` and renders Gold-tier data as interactive business charts and KPI cards.

**Dashboard capabilities:**

| View | Description |
|------|-------------|
| **Sales Funnel** | Sankey/funnel chart: view → cart → checkout → purchase drop-off by device type |
| **Revenue Trends** | Time-series area chart: daily/weekly revenue by product category |
| **Customer Cohorts** | Retention heatmap: which acquisition months produced the most loyal customers? |
| **Product Leaderboard** | Sortable table: top products by views, cart rate, and revenue |
| **Real-time Event Feed** | Near-real-time latest events polled from Bronze via Athena |

**Result caching pattern (FinOps):**
```python
@st.cache_data(ttl=300)  # cache for 5 minutes
def load_daily_revenue(start_date, end_date):
    # Athena is only queried once per 5-minute window
    # Repeat dashboard interactions within this window: $0 Athena cost
    return pd.read_sql(query, conn, params=[start_date, end_date])
```

**Hosting:** EC2 t3.micro (within Free Tier) or AWS App Runner, deployed inside the same VPC as the data platform for private Athena/S3 connectivity without public internet exposure.

---

### 4.8. Governance, Security & Monitoring

**IAM - Least-Privilege Service Roles**

| Service | IAM Permissions (scoped) |
|---------|--------------------------|
| Lambda (Ingestion) | `firehose:PutRecord` on specific Firehose stream only |
| Lambda (DB Extractor) | `s3:PutObject` on Bronze `/orders/` prefix only + `secretsmanager:GetSecretValue` on specific ARN |
| Glue ETL Job 1 | `s3:GetObject` Bronze + `s3:PutObject` Silver + `glue:UpdateTable` Silver tables only |
| Glue ETL Job 2 | `s3:GetObject` Silver + `s3:PutObject` Gold + `glue:UpdateTable` Gold tables only |
| Athena | `s3:GetObject` Silver+Gold + `s3:PutObject` results bucket + `glue:GetTable/GetPartitions` |
| Streamlit | `athena:StartQueryExecution`, `athena:GetQueryResults`, `s3:GetObject` results only |

No wildcard `s3:*` permissions anywhere. Cross-tier write access is architecturally impossible.

**KMS - Envelope Encryption Per Tier**

Three separate Customer Managed Keys (CMKs):
- `finops/bronze-cmk` → encrypts Bronze bucket
- `finops/silver-cmk` → encrypts Silver bucket
- `finops/gold-cmk` → encrypts Gold bucket

All key usage events logged to CloudTrail → CloudWatch Logs for tamper-proof audit trail.

**CloudWatch - Pipeline Observability**

*Alarms:*
| Alarm | Metric | Threshold | Alert |
|-------|--------|-----------|-------|
| Lambda error rate | `Errors/Invocations` | > 5% / 5 min | SNS email |
| Glue Job failure | `numFailedTasks` | > 0 | SNS email |
| Firehose throttling | `ThrottledRecords` | > 100/min | SNS email |
| Athena query timeout | `QueryExecutionTime` | > 60s | CloudWatch log |

*Unified CloudWatch Dashboard:* Lambda invocation rates, Glue DPU consumption, Athena queries/day, data scanned/day, S3 storage growth per tier - all in one operational view.

---

## 5. Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| **Phase 1 - Architecture Design & IaC Scaffolding** | Week 1–2 | CDK stack: S3 buckets (×3), IAM roles (×6), KMS CMKs (×3), Glue Data Catalog, VPC configuration |
| **Phase 2 - Streaming Ingestion (Path A)** | Week 3–4 | API Gateway REST API + JSON Schema validator; Firehose delivery stream; Lambda transformation (128 MB, in-flight Snappy); end-to-end test: POST event → Bronze S3 verified |
| **Phase 3 - Batch Ingestion (Path B)** | Week 5 | EventBridge Scheduler rule; Lambda DB extractor with watermark logic + SSM Parameter Store; Parquet conversion with PyArrow; Bronze verified for both streaming and batch prefixes |
| **Phase 4 - Glue ETL Processing Layer** | Week 6–7 | Glue ETL Job 1: deduplication + schema enforcement + Silver Parquet output + Catalog registration; Glue ETL Job 2: KPI aggregations + Gold output + Catalog registration; end-to-end pipeline run verified |
| **Phase 5 - Query Layer & Dashboard** | Week 8–9 | Athena Workgroup with cost controls; Gold-tier table queries verified; Streamlit Dashboard with all 5 KPI views live; PyAthena connection with 5-min cache |
| **Phase 6 - Governance & Hardening** | Week 10 | KMS CMK per tier enforced; IAM Access Analyzer scan; CloudWatch Alarms + Dashboard active; full end-to-end smoke test from raw event → Streamlit chart |

**Total duration: 10 weeks** (aligned with the FCJ Data Engineer Internship period)

**Milestone checkpoints:**

```
Week 2  ──► IaC foundation complete (cdk deploy runs without error)
Week 4  ──► First real event reaches S3 Bronze via streaming path
Week 5  ──► First batch order record lands in S3 Bronze via DB sync
Week 7  ──► Full Bronze → Silver → Gold pipeline runs end-to-end
Week 9  ──► Streamlit Dashboard displaying live Gold-tier KPIs
Week 10 ──► Platform hardened, monitored, and documented
```

---

## 6. Budget Estimation

The architecture is designed to remain under **$10/month** at internship-scale workloads (~100,000 events/day, ~1 GB/day ingested, 2 Glue job runs/day, ~50 Athena queries/day).

| # | Service | Estimated Usage | Monthly Cost |
|---|---------|----------------|-------------|
| 1 | Amazon API Gateway | 3M requests/month | ~$3.50 |
| 2 | Amazon Data Firehose | 1 GB/day × 30 = 30 GB | ~$0.90 |
| 3 | AWS Lambda | ~150K invocations, 128 MB, avg 500ms | **$0.00** (Free Tier: 1M req/month) |
| 4 | Amazon EventBridge Scheduler | 60 invocations/month | **$0.00** (Free Tier: 14M/month) |
| 5 | Amazon S3 (3 buckets) | ~30 GB total stored | ~$0.69 |
| 6 | AWS Glue ETL Jobs | 2 jobs × 2 DPUs × 30 min × 30 days | ~$0.88 |
| 7 | AWS Glue Data Catalog | < 1M objects | **$0.00** (Free Tier) |
| 8 | Amazon Athena | ~10 GB scanned/month (Parquet optimized) | **~$0.05** |
| 9 | Amazon CloudWatch | Default metrics + 5 custom alarms | ~$0.30 |
| 10 | AWS KMS | 3 CMKs + ~10K API calls | ~$0.30 |
| 11 | AWS Secrets Manager | 1 secret | ~$0.40 |
| | **Total** | | **~$7.02/month** |

> **FinOps note on Athena cost:** Without Parquet and partitioning, querying the same 30 GB of raw JSON data would cost approximately **$0.15/TB × 30 GB/day × 30 days = ~$1.35/month** - a 27× cost increase vs. the optimized $0.05/month. Parquet + partitioning is the single highest-ROI optimization in this architecture.

**AWS Free Tier coverage:** Lambda, EventBridge Scheduler, and Glue Data Catalog fall entirely within the AWS Free Tier at internship scale - three key services with $0 effective cost.

See detailed cost estimate at [AWS Pricing Calculator](https://calculator.aws).

---

## 7. Risk Assessment

### 7.1. Risk Matrix

| # | Risk | Probability | Impact | Severity |
|---|------|-------------|--------|----------|
| R1 | Lambda timeout during Firehose inline transformation (payload too large / processing too slow) | Low | Medium | **Medium** |
| R2 | Glue ETL Job DPU cost overrun from unexpectedly large dataset | Medium | Medium | **Medium** |
| R3 | Athena query scan cost spike from accidental full-table scan on Bronze or Silver | Low | High | **High** |
| R4 | S3 Bronze data loss (accidental deletion or bucket misconfiguration) | Very Low | Critical | **High** |
| R5 | DB extractor watermark drift causing duplicate or missed records | Medium | Medium | **Medium** |
| R6 | IAM misconfiguration granting cross-tier write access | Low | High | **High** |
| R7 | Firehose delivery failures causing data loss in transit | Low | Medium | **Medium** |
| R8 | Streamlit Dashboard query volume causing unexpected Athena cost | Medium | Low | **Low** |

### 7.2. Mitigation Strategies

**R1 - Lambda Timeout in Firehose Transformation**
- Set Firehose Lambda timeout to 60 seconds (well within Firehose's 5-minute maximum)
- Keep Lambda memory at 128 MB; profile transformation logic to ensure it completes in < 10 seconds per batch
- Implement **soft-fail pattern**: if Lambda returns an error, Firehose falls back to delivering the original (untransformed) record rather than dropping it - preventing data loss at the cost of a downstream data quality flag

**R2 - Glue ETL Job DPU Cost Overrun**
- Set `MaxCapacity` cap in Glue job configuration (e.g., maximum 4 DPUs per job run)
- Enable **Glue Job Bookmarks** to only process new partitions since the last successful run - preventing full re-scans on every trigger
- Monitor `glue.driver.jvm.heap.usage` via CloudWatch; set alarm if DPU-hours exceed budget threshold
- Consider **Glue Serverless (Flex)** execution class for non-urgent jobs - up to 34% cheaper than standard

**R3 - Athena Scan Cost Spike**
- Enforce a **per-query data scan limit** via Athena Workgroup (e.g., 1 GB maximum per query) - any query exceeding this is automatically cancelled before scan completes
- All dashboard queries **must** target the Gold tier only; Silver and Bronze are only accessed during ad-hoc debugging by authorized engineers
- Enable **Athena query result reuse** - queries with identical SQL within 24 hours return cached results at $0 additional scan cost
- Use `@st.cache_data(ttl=300)` in Streamlit to prevent per-user-interaction query re-execution

**R4 - S3 Bronze Data Loss**
- Enable **S3 Versioning** on the Bronze bucket - any accidental `DeleteObject` creates a delete marker, allowing recovery to any previous version
- Enable **S3 Object Lock** (Governance mode) with a 30-day retention period on Bronze objects - prevents deletion by any IAM principal (including administrators) for 30 days
- Consider **Cross-Region Replication** for production: automatically replicate Bronze objects to a second AWS region as a disaster recovery copy

**R5 - DB Extractor Watermark Drift**
- Persist watermark timestamp to **AWS SSM Parameter Store** with atomic writes - if Lambda fails mid-extraction, the watermark is not advanced, ensuring the next run re-processes the failed window
- Use **`batch_id=UUID`** as a partition key in Bronze for all batch writes - enables Glue ETL Job 1 to use batch_id-based deduplication even if the same records are extracted twice
- Implement a **reconciliation check**: after each extraction, count extracted records and compare to a `SELECT COUNT(*)` on the DB for the same time window; log discrepancies

**R6 - IAM Misconfiguration**
- All IAM roles defined exclusively in **AWS CDK IaC** - no manual console changes permitted; role permissions are version-controlled in Git
- Run **AWS IAM Access Analyzer** weekly to automatically flag any resource-based policies that grant broader-than-intended access
- No IAM role has `"Action": "*"` or `"Resource": "*"` - enforced by a CDK `NagPack` rule that fails `cdk synth` if wildcard permissions are detected

**R7 - Firehose Delivery Failures**
- Enable Firehose's built-in **S3 backup** for failed records - any record Firehose cannot deliver to the primary destination is automatically written to a separate `_failed/` S3 prefix for manual investigation
- Set a **CloudWatch Alarm** on the `DeliveryToS3.DataFreshness` metric - alerts if data is buffered in Firehose for longer than 15 minutes (indicating a delivery blockage)

**R8 - Streamlit Dashboard Query Cost**
- Implement `@st.cache_data(ttl=300)` on all Athena query functions - limits Athena invocations to once per 5-minute window per unique query signature
- Configure Athena Workgroup with a **per-workgroup monthly data scan budget** with an SNS alert at 80% of budget - proactive warning before cost overrun occurs
