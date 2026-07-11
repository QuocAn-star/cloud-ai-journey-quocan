---
title: "Proposal"
date: 2026-06-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# FinOps-Optimized Serverless Medallion Data Lakehouse Architecture for Customer Behavior Analytics

---

## 1. Project Overview

This proposal presents the end-to-end design and implementation of a **fully serverless, cloud-native data lakehouse** on AWS—specifically built for customer behavior analytics in the e-commerce sector. The platform is named **"FinOps-Optimized Serverless Medallion Data Lakehouse"** to reflect two core design principles ingrained in every architectural decision:

1. **FinOps-first (Cost optimization is the top priority)**: Every AWS service choice is selected to minimize costs—serverless compute (no idle costs), on-demand querying, in-flight data transformation to eliminate intermediate storage writes, and intelligent S3 storage tiering. The platform delivers production-grade analytics with an estimated total cost of under **$8/month** at an internship scale.
2. **Medallion Architecture**: Raw data flows through three progressively refined S3 layers—**Bronze** (raw, immutable landing zone) → **Silver** (cleaned, schema-validated) → **Gold** (business-aggregated, analytics-ready)—ensuring data quality improves at each stage while retaining the ability to replay the entire pipeline from raw data at any time.

The platform consolidates **two ingestion streams**: real-time clickstream events from web and mobile applications (streaming flow via API Gateway → Firehose) and periodic order records from the transactional database (batch flow via EventBridge → Lambda). Both streams land in the same S3 Bronze bucket, ensuring a single source of truth regardless of data origin. Downstream, Glue ETL Jobs transform data across the Medallion layers, Amazon Athena provides serverless SQL analytics, and a **Streamlit Dashboard** presents business-ready KPIs to stakeholders.

> **Overall Architecture Diagram:**

![FinOps-Optimized Serverless Medallion Data Lakehouse Architecture](/images/2-Proposal/Architecture_DE.png)

**Platform Overview:**

| Dimension | Details |
|---|---|
| **Use case** | E-commerce customer behavior analytics |
| **Ingestion** | Real-time streaming (clickstream) + Scheduled batch (orders) |
| **Storage pattern** | Medallion Architecture: Bronze → Silver → Gold on Amazon S3 |
| **Processing** | AWS Glue ETL (PySpark) - serverless, billed per DPU-second |
| **Analytics** | Amazon Athena - serverless SQL, billed per TB scanned |
| **Visualization** | Python Streamlit Dashboard via PyAthena |
| **IaC** | AWS CDK (TypeScript) - entire platform defined as code |
| **Estimated cost** | ~$7–8/month at internship scale |
| **Governance** | Least-privilege IAM + KMS CMKs + CloudWatch observability |

---

## 2. Objectives

The platform is designed to achieve the following measurable objectives:

### 2.1. Technical Objectives

**OBJ1 - Consolidated dual-stream ingestion:**
Build and validate two separate ingestion streams that both land in a single S3 Bronze bucket:
- Streaming stream: real-time clickstream from web/mobile → API Gateway → Firehose + Lambda → S3 Bronze, with sub-second edge validation and in-flight transformation.
- Batch stream: transactional order records → EventBridge Scheduler → Lambda DB extractor (watermark-based) → S3 Bronze, on a configurable hourly/daily cycle.

**OBJ2 - Three-tier Medallion data quality pipeline:**
Implement two sequential AWS Glue ETL Jobs that progressively refine data quality:
- **Glue ETL Job 1 (Bronze → Silver)**: deduplication, null handling, schema enforcement, type casting, conversion to Parquet with Snappy compression.
- **Glue ETL Job 2 (Silver → Gold)**: business KPI aggregation - daily revenue by category, user funnel conversion rates, customer LTV segmentation, product performance metrics.

**OBJ3 - Serverless SQL analytics with FinOps optimization:**
Configure Amazon Athena with a dedicated Workgroup enforcing data scan limits per query, combined with Parquet columnar format and Hive-style partitioning to effectively reduce scanned data by 85–90% compared to raw JSON - delivering sub-second query performance on Gold tier data at minimal cost.

**OBJ4 - Interactive Streamlit Dashboard:**
Develop a Python Streamlit web application connecting to Athena via `pyathena` displaying at least 5 business KPIs (sales funnel, revenue trends, product leaderboard, customer cohort analysis, near real-time event stream) with 5-minute result caching to minimize repetitive query costs.

**OBJ5 - Infrastructure as Code (IaC):**
Define the entire platform - S3 buckets, IAM roles, KMS keys, Glue resources, API Gateway, Lambda, Firehose, EventBridge, Athena Workgroup - as CDK TypeScript constructs, enabling repeatable one-command deploy (`cdk deploy`) and destroy (`cdk destroy`).

**OBJ6 - Governance and observability:**
Implement least-privilege IAM roles per service, AWS KMS Customer Managed Keys per S3 tier, and a CloudWatch Dashboard with alarms covering Lambda error rates, Glue Job failures, Firehose throttling, and Athena query timeouts.

### 2.2. Learning Objectives

Beyond technical deliverables, this project is a hands-on learning experience during the internship to develop competencies:

| Skill Area | AWS Service / Tool |
|---|---|
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

Modern e-commerce businesses generate massive volumes of data every second - from real-time clickstream events on websites and mobile apps (page views, product clicks, add to cart, checkout completions) to transactional order records stored in relational backend databases. When properly harnessed, this data unlocks powerful insights into customer behavior patterns, sales funnel conversion rates, product performance, and operational efficiency.

However, for small to medium-sized e-commerce teams (and internship-scale projects operating on limited AWS credits), accessing these insights is hindered by an interconnected set of infrastructural challenges:

### 3.2. Five Core Problems

**Problem 1 - Dual data velocities without a unified landing zone**
Clickstream events arrive continuously at variable rates (0 to thousands of events/second), requiring low-latency high-throughput streaming ingestion. Order records, conversely, are generated by transactional OLTP databases that cannot be queried continuously without degrading production performance - requiring a scheduled batch extraction pattern.
Without a platform handling both, teams are forced to choose: build two separate pipelines with separate storage, or batch everything and lose real-time behavioral signals.

**Problem 2 - Data quality degradation without an enforcement layer**
Client-generated event payloads are inherently unreliable: they may contain invalid JSON, missing mandatory fields, invalid data types, duplicate event IDs (from client retry logic), or outdated timestamps. Without a validation and transformation layer, these errors propagate silently into downstream analytics - corrupting KPIs, inflating user counts, and leading to misguided business decisions.

**Problem 3 - Cost vs. scale tension with traditional approaches**
Traditional analytics solutions for this use case (e.g., always-on Redshift clusters, continuously running EMR clusters, fixed Kafka brokers) incur significant fixed costs regardless of actual processing or query volume. With a limited AWS credit budget and highly variable workloads (low at night, high during business hours), this fixed-cost model is economically unsustainable.

| Traditional Approach | Estimated Cost/Month | Issue |
|---|---|---|
| Amazon Redshift (ra3.xlplus, 2 nodes) | ~$700–900/month | Massive over-provisioning for internship scale |
| Amazon EMR (m5.xlarge, 3 nodes) | ~$300–500/month | Idle cluster costs between batch runs |
| Amazon MSK (kafka.m5.large, 3 brokers) | ~$400–600/month | 24/7 costs even when no events are flowing |
| **This platform (fully serverless)** | **~$7–8/month** | **Only pay for actual usage** |

**Problem 4 - Lack of centralized governance or access control**
Without a structured platform, data engineers tend to apply S3 bucket policies and IAM permissions in an ad-hoc manner - leading to "permission sprawl" as services accumulate more access rights than necessary. Sensitive customer data (email addresses, purchase history, behavioral profiles) becomes accessible to any team member or service with S3 read access, violating the principle of least privilege and creating compliance risks.

**Problem 5 - No schema management or query optimization**
Raw JSON data stored in S3 lacks an associated schema catalog, making it impossible for SQL tools like Athena to understand table structures without manual `CREATE TABLE` statements. Furthermore, querying raw JSON with Athena is significantly more expensive than querying Parquet (Athena charges per TB scanned - JSON files are 5–10 times larger than equivalent Parquet files for the same logical data).

### 3.3. Why This Matters

Without resolving these five problems, e-commerce analytics capabilities remain:
- **Non-existent** (no platform built) - business decisions based on gut feeling, not data.
- **Fragile** (ad-hoc scripts, manual SQL) - irreproducible, unscalable, ungoverned.
- **Expensive** (always-on clusters) - unsustainable on internship-scale AWS credits.

This proposal simultaneously addresses all five problems through a serverless, IaC-defined, consistent data lakehouse that is both cost-effective and production-ready.

---

## 4. Solution Architecture

### 4.1. Architecture Overview

The platform is organized into **six functional layers** plus a **horizontal governance layer**, each with precisely defined responsibilities:

| Layer | AWS Service | Responsibility |
|---|---|---|
| **Data Source** | Website, Mobile App, E-commerce Orders DB | Generate events and transactional records |
| **Ingestion Layer** | API Gateway, Data Firehose, Lambda, EventBridge Scheduler | Dual-stream data collection and edge validation |
| **Storage Layer** | Amazon S3 (Bronze / Silver / Gold) | Immutable data lake storage by Medallion tier |
| **Processing Layer** | AWS Glue ETL Jobs, Glue Data Catalog | Schema transformation and business aggregation |
| **Query Layer** | Amazon Athena, Glue Data Catalog | Serverless SQL analytics over S3 |
| **Visualization Layer** | Streamlit Dashboard | Interactive business KPI exploration |
| **Governance** | AWS IAM, AWS KMS, Amazon CloudWatch | Security, encryption, and observability |

---

### 4.2. Data Sources

**Source 1 - Website & Mobile App (Real-time Events)**

User-facing web and mobile applications continuously emit behavioral events - page views, product detail views, add to cart, initiate checkout, purchase completion, and session end. Each event is a structured JSON payload sent via HTTP POST to the ingestion endpoint. Volumes are highly variable: near zero at 3 AM, spiking during flash sales.

- **Format**: JSON, schema versioned by event type
- **Velocity**: 0 to thousands of events/sec (unpredictable)
- **Latency requirement**: Sub-second ingestion; analytics acceptable within minutes
- **Quality risks**: Invalid JSON, missing mandatory fields, wrong data types from client bugs

**Source 2 - Orders Database (Batch Records)**

A transactional relational database (PostgreSQL/MySQL) stores completed order records including order ID, customer ID, SKU, quantity, price, payment status, and completion timestamp. It cannot be continuously queried without degrading production OLTP performance.

- **Format**: Relational rows → extracted to Apache Parquet
- **Velocity**: Batch, hourly or daily extraction
- **Latency requirement**: T+1 hour is acceptable
- **Quality risks**: Duplicate records from retry logic, partial updates from long-running transactions

---

### 4.3. Ingestion Layer

**Stream A - Web / Mobile Streaming** *(Steps 1 → 2 → 3)*

**Step 1 - Amazon API Gateway: Edge Ingestion & Validation**

All client events enter via an HTTP POST endpoint on **Amazon API Gateway** (REST API). A **Request Validator** enforces strict **JSON Schema** at the edge - invalid requests are immediately rejected with `400 Bad Request` before reaching any downstream services.

> **FinOps Impact**: Validation at API Gateway incurs no additional cost - bad data is rejected before Lambda or Firehose is invoked, preventing wasted downstream compute.

**Step 2 - Amazon Data Firehose + AWS Lambda: Buffering & In-line Transformation**

Validated payloads flow into an **Amazon Data Firehose** delivery stream. Firehose is chosen over Kinesis Data Streams because it requires no shard capacity planning, natively buffers and batches records prior to S3 delivery, and supports synchronous in-line Lambda invocation.

Firehose synchronously invokes a lightweight **AWS Lambda** (128 MB RAM) for in-flight transformation:
- Standardize event timestamps to UTC ISO-8601
- Enrich records with pipeline metadata
- Soft-validate secondary fields (flagging anomalies without dropping records)
- Return transformed records **in-memory** - no intermediate S3 writes

> **FinOps Impact**: In-RAM Lambda transformation eliminates the intermediate S3 PUT+GET cycle that traditional "write then read" pipelines incur.

**Step 3 - S3 Bronze Bucket: Streaming Destination**

Firehose flushes the buffered records as **NDJSON**, partitioned by the following prefix:
```text
s3://[project]-bronze/events/year=YYYY/month=MM/day=DD/hour=HH/
```

The bronze bucket is **raw and immutable**—data is stored exactly as received, serving as the single source of truth for reprocessing the entire pipeline.

---
**Flow B - DB / Batch Synchronization** *(Step 8 → Lambda → S3 Bronze)*

**Step 8 - Amazon EventBridge Scheduler: Orchestration Trigger**

An **EventBridge Scheduler** rule triggers based on a cron expression (e.g., `rate(1 hour)`). There is no always-running infrastructure—no EC2 instances, containers, or persistent processes. Costs are incurred only during the execution window.

**AWS Lambda - DB Extraction Function**

The trigger invokes a **Lambda function** that performs the following:
1. Retrieves DB credentials from **AWS Secrets Manager** (never hardcoded).
2. Queries records using the **watermark pattern**: `WHERE updated_at > last_successful_run_timestamp`.
3. Converts the result set into **Apache Parquet** format in-memory using PyArrow.
4. Writes the Parquet file to S3 Bronze under a logically partitioned prefix:
```
s3://[project]-bronze/orders/year=YYYY/month=MM/day=DD/batch_id=UUID/
```
5. Saves the new watermark timestamp to **AWS SSM Parameter Store** to enable idempotent re-runs.


---

### 4.4. Storage Layer - Medallion Architecture

The platform implements the **Medallion Architecture** - each S3 tier represents an increasingly higher level of quality and business readiness:

| Tier | S3 Bucket | Format | Partitioning | Description |
|------|-----------|-----------|-----------|-------|
| **Bronze** | `[proj]-bronze` | NDJSON (stream) / Parquet (batch) | `year/month/day/hour` | Raw, immutable. Always capable of full reprocessing from here. |
| **Silver** | `[proj]-silver` | Parquet + Snappy | `year/month/day` | Cleaned, deduplicated, schema-validated. Optimized for querying. |
| **Gold** | `[proj]-gold` | Parquet + Snappy | `metric_date/category` | Pre-aggregated KPIs. Directly consumed by the visualization layer. |

**Why Parquet + Snappy?**
- Reduces storage by up to **87%** compared to raw JSON → lower S3 costs
- **Column pruning**: Athena only reads accessed columns → less data scanned → lower query costs
- **Predicate pushdown**: Athena skips row groups that do not match the WHERE filter → faster and cheaper

**Examples of generated Gold datasets:**
- `daily_revenue_by_category` - daily revenue by product category
- `user_funnel_daily` - user counts at each funnel stage (view → cart → checkout → purchase)
- `customer_ltv_segments` - 90-day cumulative customer lifetime value grouped into LTV tiers
- `product_performance_weekly` - view-to-purchase conversion rate by product, trailing 7 days

**Security:** All three buckets are encrypted at rest using **AWS KMS Customer Managed Keys (CMKs)** - a separate CMK for each tier. S3 bucket policies enforce zero cross-tier write permissions.

---

### 4.5. Processing Layer - AWS Glue ETL Pipelines

**Glue ETL Job 1 - Bronze → Silver Transformation (Step 5)**

Triggered by EventBridge after batch ingestion completes. Reads from Bronze, applies:
1. **Schema enforcement** - cast fields to canonical data types
2. **Deduplication** - window function on `event_id` / `order_id`, keeping the most recent
3. **Null handling** - fill optional nulls with defaults; quarantine records missing mandatory fields to a `_quarantine/` prefix
4. **String normalization** - lowercase for categories, standardize phone/email formats
5. **Format conversion** - output Parquet + Snappy, partitioned by `year/month/day`

When complete: invokes the Glue Data Catalog API to register the new Silver partitions - **no Crawler required**.

**Glue ETL Job 2 - Silver → Gold Aggregation (Step 6)**

Runs after Job 1. Reads from Silver, computes:
1. Revenue aggregation: `SUM(order_total) GROUP BY (category, order_date)`
2. Funnel analysis: distinct user counts by `event_type` per day + stage conversion rates
3. Customer LTV segmentation: total cumulative 90-day spend by `customer_id` → LTV segment labels
4. Product performance: view-to-purchase conversion rate by `product_id` in a trailing 7-day window
5. Sessionization: group clickstream events into sessions (30-minute inactivity window) → compute session duration and pages/session

When complete: registers the Gold table partitions in the Glue Data Catalog.

**Glue Data Catalog (Step 7)**

The central metadata repository for all three tiers. Stores table schemas, partition keys, and S3 physical locations. Both ETL Jobs register output directly via the Catalog API - **no scheduled Crawlers**, eliminating DPU-hour crawl costs. Amazon Athena reads from the Catalog to plan optimal query execution without moving data.

---

### 4.6. Query Layer - Amazon Athena

Amazon Athena provides **interactive, serverless SQL analytics** directly on S3 data - no clusters, no provisioning, pay only per TB scanned.

**FinOps Optimization Stack for Athena:**

| Optimization | Mechanism | Cost Impact |
|-----------|--------|----------------|
| Parquet Columnar Format | Silver + Gold stored as Parquet | Reduces scanned data by 70–90% compared to JSON |
| Snappy Compression | All Parquet files are compressed | Smaller S3 objects → less data transferred |
| Hive Partitioning | Partition key `year/month/day` | Athena eliminates irrelevant partitions before scanning |
| Pre-aggregated Gold Tier | Dashboard queries target Gold | Scans thousands of rows vs. millions of raw events |
| Query Result Reuse | Athena result caching enabled | Identical queries within 24h return cached results for $0 |
| Workgroup Scan Limit | Per-query data scan cap (e.g., max 1 GB) | Prevents runaway queries from consuming credits |

Athena is programmatically accessed by Streamlit via `pyathena` (DBAPI2 interface) with parameterized SQL. Results are stored in a dedicated S3 results bucket for audit trails and caching.

---

### 4.7. Visualization Layer - Streamlit Dashboard

A **Python Streamlit web application** connects to Athena via `pyathena` and displays Gold tier data as interactive business charts and KPI cards.

**Dashboard Capabilities:**

| View | Description |
|------|-------|
| **Sales Funnel** | Sankey/funnel chart: drop-off view → cart → checkout → purchase by device type |
| **Revenue Trends** | Time-series line chart: daily/weekly revenue by product category |
| **Customer Cohort** | Retention heatmap: which acquisition month generates the most loyal customers? |
| **Product Leaderboard** | Sortable table: top products by views, add-to-cart rate, and revenue |
| **Near Real-Time Event Stream** | Latest events from Bronze polled via Athena |

**Result Caching Pattern (FinOps):**
```python
@st.cache_data(ttl=300)  # cache for 5 minutes
def load_daily_revenue(start_date, end_date):
    # Athena is queried only once every 5 minutes
    # Repeated dashboard interactions within this window: $0 Athena cost
    return pd.read_sql(query, conn, params=[start_date, end_date])

```

**Hosting:** EC2 t3.micro (within the Free Tier) or AWS App Runner, deployed in the same VPC as the data platform to enable private connectivity to Athena/S3 without using the public internet.

---

### 4.8. Governance, Security & Monitoring

**IAM - Least-Privilege IAM Roles**

| Service | Scoped IAM Permissions |
|---------|----------------------|
| Lambda (Ingestion) | `firehose:PutRecord` only on the specific Firehose stream |
| Lambda (DB Extractor) | `s3:PutObject` on Bronze prefix `/orders/` + `secretsmanager:GetSecretValue` for specific ARN |
| Glue ETL Job 1 | `s3:GetObject` on Bronze + `s3:PutObject` on Silver + `glue:UpdateTable` only for Silver table |
| Glue ETL Job 2 | `s3:GetObject` on Silver + `s3:PutObject` on Gold + `glue:UpdateTable` only for Gold table |
| Athena | `s3:GetObject` on Silver+Gold + `s3:PutObject` on results bucket + `glue:GetTable/GetPartitions` |
| Streamlit | `athena:StartQueryExecution`, `athena:GetQueryResults`, `s3:GetObject` only on results |

No wildcard `s3:*` permissions anywhere. Cross-tier write access is architecturally impossible.

**KMS - Tiered Envelope Encryption**

Three distinct Customer Managed Keys (CMKs):
- `finops/bronze-cmk` → encrypts Bronze bucket
- `finops/silver-cmk` → encrypts Silver bucket
- `finops/gold-cmk` → encrypts Gold bucket

All key usage events are logged to CloudTrail → CloudWatch Logs for a tamper-proof audit trail.

**CloudWatch - Pipeline Observability**

*Alarms:*
| Alarm | Metric | Threshold | Alert |
|-------|--------|--------|---------|
| Lambda Error Rate | `Errors/Invocations` | > 5% / 5 mins | SNS email |
| Glue Job Failure | `numFailedTasks` | > 0 | SNS email |
| Firehose Throttling | `ThrottledRecords` | > 100/min | SNS email |
| Athena Query Timeout | `QueryExecutionTime` | > 60s | CloudWatch log |

*Unified CloudWatch Dashboard:* Lambda invocation rates, Glue DPU consumption, Athena queries/day, data scanned/day, S3 storage growth by tier - all in a single operational view.

---

## 5. Timeline

| Phase | Duration | Key Deliverables |
|-----------|-----------|-------------------|
| **Phase 1 - Architecture Design & IaC Scaffolding** | Weeks 1–2 | CDK stack: S3 buckets (×3), IAM roles (×6), KMS CMKs (×3), Glue Data Catalog, VPC configuration |
| **Phase 2 - Streaming Ingestion (Stream A)** | Weeks 3–4 | API Gateway REST API + JSON Schema validator; Firehose delivery stream; Lambda transformation (128 MB, in-flight Snappy); end-to-end testing: POST event → Bronze S3 verification |
| **Phase 3 - Batch Ingestion (Stream B)** | Week 5 | EventBridge Scheduler rule; Lambda DB extractor with watermark logic + SSM Parameter Store; Parquet conversion with PyArrow; Bronze verification for both streaming and batch prefixes |
| **Phase 4 - Glue ETL Processing Layer** | Weeks 6–7 | Glue ETL Job 1: deduplication + schema enforcement + Silver Parquet output + Catalog registration; Glue ETL Job 2: KPI aggregations + Gold output + Catalog registration; verified end-to-end pipeline run |
| **Phase 5 - Query Layer & Dashboard** | Weeks 8–9 | Athena Workgroup with cost controls; Gold tier table queries verified; Streamlit Dashboard with all 5 active KPI views; PyAthena connectivity with 5-minute caching |
| **Phase 6 - Governance & Hardening** | Week 10 | Tiered KMS CMKs enforced; IAM Access Analyzer scan; CloudWatch Alarms + Dashboard live; full end-to-end smoke test from raw event → Streamlit chart |

**Total Timeline: 10 weeks** (aligned with FCJ Data Engineer internship duration)

**Milestones:**

```text
Week 2  ──► IaC Foundation complete (cdk deploy runs error-free)
Week 4  ──► First live event lands in S3 Bronze via streaming flow
Week 5  ──► First batch order records land in S3 Bronze via DB sync
Week 7  ──► Full Bronze → Silver → Gold pipeline runs end-to-end
Week 9  ──► Streamlit Dashboard displays live Gold tier KPIs
Week 10 ──► Platform hardened, monitored, and documented
```

---

## 6. Budget

The architecture is designed to remain under **$10/month** at internship scale (~100,000 events/day, ~1 GB/day ingested, 2 Glue job runs/day, ~50 Athena queries/day).

| # | Service | Estimated Usage | Cost/Month |
|---|---------|----------------|--------------|
| 1 | Amazon API Gateway | 3 million requests/month | ~$3.50 |
| 2 | Amazon Data Firehose | 1 GB/day × 30 = 30 GB | ~$0.90 |
| 3 | AWS Lambda | ~150K invocations, 128 MB, avg 500ms | **$0.00** (Free Tier: 1M req/month) |
| 4 | Amazon EventBridge Scheduler | 60 calls/month | **$0.00** (Free Tier: 14M/month) |
| 5 | Amazon S3 (3 buckets) | ~30 GB total storage | ~$0.69 |
| 6 | AWS Glue ETL Jobs | 2 jobs × 2 DPUs × 30 mins × 30 days | ~$0.88 |
| 7 | AWS Glue Data Catalog | < 1 million objects | **$0.00** (Free Tier) |
| 8 | Amazon Athena | ~10 GB scanned/month (Parquet optimized) | **~$0.05** |
| 9 | Amazon CloudWatch | Default metrics + 5 custom alarms | ~$0.30 |
| 10 | AWS KMS | 3 CMKs + ~10K API calls | ~$0.30 |
| 11 | AWS Secrets Manager | 1 secret | ~$0.40 |
| | **Total** | | **~$7.02/month** |

> **FinOps Note on Athena Cost:** Without Parquet and partitioning, querying the same 30 GB of raw JSON data would cost around **$0.15/TB × 30 GB/day × 30 days = ~$1.35/month** - a 27x cost increase compared to the optimized $0.05/month. Parquet + partitioning is the highest ROI optimization in this architecture.

**AWS Free Tier Coverage:** Lambda, EventBridge Scheduler, and Glue Data Catalog fit completely within the AWS Free Tier at internship scale - three pivotal services with a $0 cost-efficiency.

See detailed cost estimates at [AWS Pricing Calculator](https://calculator.aws).

---

## 7. Risks

### 7.1. Risk Matrix

| # | Risk | Probability | Impact | Level |
|---|--------|----------|---------|--------|
| R1 | Lambda timeout during Firehose in-line transformation (payload too large / processing too slow) | Low | Medium | **Medium** |
| R2 | Glue ETL Job DPU cost overrun from unexpectedly large datasets | Medium | Medium | **Medium** |
| R3 | Athena scan cost spike from accidental full-table scans on Bronze or Silver | Low | High | **High** |
| R4 | S3 Bronze data loss (accidental deletion or bucket misconfiguration) | Very Low | Critical | **High** |
| R5 | DB extractor watermark drift causing duplicate or skipped records | Medium | Medium | **Medium** |
| R6 | IAM misconfiguration granting cross-tier write permissions | Low | High | **High** |
| R7 | Firehose delivery failures causing data loss in transit | Low | Medium | **Medium** |
| R8 | Streamlit Dashboard query volume causing unexpected Athena costs | Medium | Low | **Low** |

### 7.2. Mitigation Strategies

**R1 - Lambda Timeout in Firehose Transformation**
- Set Firehose Lambda timeout to 60 seconds (well within Firehose's 5-minute maximum limit).
- Keep Lambda memory at 128 MB; profile transformation logic to ensure completion in < 10 seconds per batch.
- Implement a **soft-fail pattern**: if Lambda returns an error, Firehose falls back to delivering the original (untransformed) record instead of dropping it - preventing data loss at the cost of downstream data quality flags.

**R2 - Glue ETL Job DPU Cost Overrun**
- Set `MaxCapacity` limits in the Glue job configuration (e.g., max 4 DPUs per run).
- Enable **Glue Job Bookmarks** to only process new partitions since the last successful run - preventing full re-scans on every trigger.
- Monitor `glue.driver.jvm.heap.usage` via CloudWatch; set an alarm if DPU-hours exceed the budget threshold.
- Consider **Glue Serverless (Flex)** execution class for non-urgent jobs - up to 34% cheaper than standard.

**R3 - Athena Scan Cost Spike**
- Enforce a **data scan limit per query** via the Athena Workgroup (e.g., max 1 GB) - any query exceeding this is automatically killed before completion.
- All dashboard queries **must** target the Gold tier; Silver and Bronze are only accessed for ad-hoc debugging by authorized engineers.
- Enable **Athena query result reuse** - identical SQL queries within 24 hours return cached results at zero additional scan cost.
- Use `@st.cache_data(ttl=300)` in Streamlit to prevent query re-execution on every user interaction.

**R4 - S3 Bronze Data Loss**
- Enable **S3 Versioning** on the Bronze bucket - any accidental `DeleteObject` creates a delete marker, allowing recovery to any previous version.
- Enable **S3 Object Lock** (Governance mode) with a 30-day retention period on Bronze objects - preventing deletion by any IAM principal (including admin) for 30 days.
- Consider **Cross-Region Replication** for production: automatically copy Bronze objects to a second AWS region as a disaster recovery backup.

**R5 - DB Extractor Watermark Drift**
- Store the watermark timestamp in **AWS SSM Parameter Store** with atomic writes - if the Lambda fails midway, the watermark is not advanced, ensuring the next run re-processes the failed window.
- Use a **`batch_id=UUID`** as a partition key in Bronze for all batch writes - allowing Glue ETL Job 1 to use deduplication based on `batch_id` even if the same records are extracted twice.
- Implement a **reconciliation check**: after each extraction, count extracted records and compare with a `SELECT COUNT(*)` on the DB for the same time window; log discrepancies.

**R6 - IAM Misconfiguration**
- All IAM roles are defined exclusively in **AWS CDK IaC** - no manual console changes allowed; role permissions are version-controlled in Git.
- Run **AWS IAM Access Analyzer** weekly to automatically flag any resource-based policies granting broader access than intended.
- No IAM role has `"Action": "*"` or `"Resource": "*"` - enforced by CDK `NagPack` rules that fail `cdk synth` if wildcards are detected.

**R7 - Firehose Delivery Failures**
- Enable Firehose's built-in **S3 backup** for failed records - any record Firehose cannot deliver to the primary destination is automatically written to a separate `_failed/` S3 prefix for manual investigation.
- Set a **CloudWatch Alarm** on the `DeliveryToS3.DataFreshness` metric - alert if data is buffered in Firehose for longer than 15 minutes (indicating delivery bottlenecks).

**R8 - Streamlit Dashboard Query Costs**
- Implement `@st.cache_data(ttl=300)` on all Athena query functions - limiting Athena invocations to once every 5 minutes per unique query signature.
- Configure the Athena Workgroup with a **monthly workgroup data scan budget** with an SNS alert at 80% of the budget - proactively alerting before cost overruns occur.
