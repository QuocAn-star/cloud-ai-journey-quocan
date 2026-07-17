---
title: "Event 2"
date: 2026-06-27
weight: 4
chapter: false
pre: " <b> 4.2. </b> "
---

# Event Report: FCAJ COMMUNITY DAY - "DATA DRIVEN, AI RISEN"

### Event Information

| Field | Details |
|-------|---------|
| **Event Name** | FCAJ COMMUNITY DAY - "DATA DRIVEN, AI RISEN" |
| **Date & Time** | 09:00, Saturday, June 27, 2026 |
| **Location** | 26th Floor, Bitexco Tower, 02 Hai Trieu Street, Saigon Ward, Ho Chi Minh City |
| **Role** | Attendee |

---

### Speakers

- **Truong Tran**
- **Steve Tran**
- **Trung Vu**
- **Anh Dang**
- **Nghi Danh**
- **Kiet Tran**
- **Bao Phan**
- **Nguyen Nguyen**
- **Toan Nguyen**

---

### Event Schedule

| Time | Topic |
|------|-------|
| 09:00 – 09:25 | Deep Response Engine: From Detection to Autonomous Resolution |
| 09:25 – 09:55 | Voice Agents: Building Human-Like AI Conversations at Scale |
| 09:55 – 10:20 | AWS DevOps Agent: Your Always-Available Operations Teammate |
| 10:20 – 10:45 | AI-Powered Productivity: Workforce Planning For Enterprise |
| 10:45 – 11:30 | Building Secure Private MCP Connection with Amazon QuickSight Q |

---

### Session Summaries

#### 1. Deep Response Engine: From Detection to Autonomous Resolution

The opening session asked a fundamental question in modern cloud operations: **what happens after an alert fires?** Rather than stopping at detection, the Deep Response Engine proposes a paradigm shift - from alert-driven systems to action-driven autonomous operations.

**The complexity wall in modern cloud operations:**
Today's cloud systems generate thousands of alerts daily. Operations teams easily fall into "alert fatigue" - overwhelmed by notifications to the point where they can't distinguish critical from noise. The result: longer MTTD and MTTR, directly impacting user experience and revenue.

**Shifting from alert-driven to action-driven:**
Instead of alerting and waiting for an engineer to respond, an action-driven system can:
- Automatically analyze root causes.
- Propose or execute remediation actions without manual intervention.
- Learn from past incidents to respond faster in the future.

**Deep Response Engine architecture:**
The system is built in multi-tier layers: data collection (metrics, logs, traces) → AI analysis → decision making → automated action execution. Each tier runs in parallel and continuously to ensure real-time responsiveness.

**Live demo - autonomous incident response:**
The live demo showed the system detecting a failing service, identifying the cause, performing an automatic rollback, and notifying the team - all within seconds, without an on-call engineer needing to wake up.

**Business impact:**
- Significant operational cost reduction through automation of repetitive tasks.
- Achieving genuine zero-downtime operations - not just on paper.
- Freeing engineers from reactive work to focus on system improvements.

---

#### 2. Voice Agents: Building Human-Like AI Conversations at Scale

This session explored the evolution of human-machine communication - from rigid IVR systems to Voice Agents capable of interacting like real people.

**The journey from IVR to AI Voice Agent:**
- **IVR (Interactive Voice Response)**: Rigid menus, users must press numbers following instructions - poor experience, high abandonment rates.
- **Text chatbots**: More flexible but still lack context and feel unnatural.
- **AI Voice Agent**: Listens, understands context, responds with natural speech, and handles complex situations in real time.

**Three core challenges:**
- **Latency**: Users expect responses within 300–500ms. Any larger delay breaks the natural conversational flow.
- **Accuracy**: Speech recognition in noisy environments, regional accents, and domain-specific terminology.
- **Natural interaction**: Handling interruptions, repetitions, mid-conversation topic changes - things humans do naturally but machines typically fail at.

**Amazon Nova Sonic - Speech-to-Speech foundation model:**
Nova Sonic is AWS's new foundation model that processes audio input and generates audio output directly, bypassing the intermediate text conversion step. This dramatically reduces latency and preserves the natural characteristics of speech - intonation, rhythm, and prosody.

**System architecture:**
`Telephony → Streaming Audio → Amazon Nova Sonic → Amazon Bedrock → MCP Tools → Response Audio`

The entire pipeline is designed to minimize latency at every stage, with the ability to scale to millions of concurrent calls.

**Enterprise use cases and demo:**
Real-world applications include automated customer service centers, appointment scheduling, and first-tier technical support. The demo showed a Voice Agent handling a complex customer request - asking clarifying questions, looking up the system, and providing an answer - all within a single continuous conversation.

---

#### 3. AWS DevOps Agent: Your Always-Available Operations Teammate

Imagine having a DevOps colleague who is available 24/7, never gets tired, and has knowledge of your entire system - that's AWS DevOps Agent.

**AWS DevOps Agent overview:**
AWS DevOps Agent is an AI Agent specialized for operations work, deeply integrated into the AWS ecosystem to assist engineers in detecting, analyzing, and resolving incidents.

**Reducing MTTD and MTTR with AI:**
- **MTTD (Mean Time To Detect)**: The Agent continuously monitors metrics, logs, and traces - detecting anomalies far earlier than a human could.
- **MTTR (Mean Time To Resolve)**: The Agent suggests solutions based on incident history and trained runbooks, enabling faster resolution.

**Supporting multi-cloud and hybrid environments:**
Not limited to the AWS ecosystem, the Agent can connect to and monitor workloads on Azure, GCP, and on-premises through integrated connectors.

**Bedrock AgentCore and multi-agent reasoning:**
The system uses Amazon Bedrock AgentCore to orchestrate multiple specialized agents working together:
- Log analysis agent.
- Configuration inspection agent.
- Runbook lookup agent.
- Remediation execution agent.

Results are synthesized and presented to the engineer as prioritized recommendations.

**ECS demo walkthrough:**
The demo depicted an ECS service failure scenario: the Agent automatically detected the issue, analyzed container logs, identified the cause as a memory leak, recommended increasing the memory limit and restarting the task - all logged in a full audit trail.

---

#### 4. AI-Powered Productivity: Workforce Planning For Enterprise

This session brought AI into the domain of human resources management - a field that has traditionally been slow to adopt new technology.

**HR transformation challenges in modern enterprises:**
- HR data scattered across multiple systems (HRIS, spreadsheets, emails).
- Workforce planning often based on gut feeling rather than data.
- Manual processes consume too much of the HR team's time, leaving little room for strategic work.

**Amazon QuickSight Q and its HR capabilities:**
Amazon QuickSight Q was presented as an AI assistant capable of:
- Answering HR questions in natural language: "What was the attrition rate last quarter?"
- Aggregating data from multiple sources and generating instant reports.
- Detecting workforce trends before they become problems.

**Accelerating HR operations with automation:**
- Automating onboarding and offboarding workflows.
- Automatically triggering performance review reminders on schedule.
- Reducing HR request processing time from days to hours.

**Workforce analytics and data-driven insights:**
Rather than backward-looking reports, the system provides predictive analytics: forecasting employee attrition risk, identifying skill gaps before they impact projects, and suggesting talent retention strategies.

**Strategic workforce planning for enterprise decision-making:**
With complete data and accurate analysis, managers can make hiring, training, and resource allocation decisions based on actual needs - rather than pure intuition.

---

#### 5. Building Secure Private MCP Connection with Amazon QuickSight Q

The final session dove into the technical and security aspects of extending Amazon QuickSight Q through the Model Context Protocol (MCP).

**Amazon QuickSight Q as an AI assistant platform:**
QuickSight Q is not just a data analytics tool - with MCP, it becomes a platform that can connect and interact with any system in the enterprise.

**What is MCP (Model Context Protocol)?**
MCP is a standardized protocol that allows AI models to connect with external data sources and tools in a controlled manner. Instead of hardcoding each integration, MCP provides a "common language" enabling AI to extend its capabilities flexibly.

**Security challenges in MCP-based integrations:**
- MCP servers by default expose over the internet - a risk when they contain sensitive enterprise data.
- Complex authentication and access control when multiple data sources are involved.
- Risk of data exfiltration without tight controls.

**Configuring Amazon QuickSight Q VPC private connectivity:**
The proposed solution uses a VPC Private Endpoint so that all traffic between QuickSight Q and the MCP server runs within AWS's internal network - never touching the public internet. Implementation steps:
1. Create a VPC and configure Security Groups for the MCP server.
2. Set up a VPC Endpoint for QuickSight Q.
3. Configure IAM roles with least-privilege permissions.
4. Verify connectivity and review audit logs.

**Demo and real-world implementation insights:**
The demo showed a QuickSight Q agent connecting to an internal database via VPC private link, executing queries, and returning results - with no traffic leaving the private network. The Q&A portion shared real-world gotchas commonly encountered during production deployments.

---

### Key Takeaways

#### On AI-driven operations
- **Autonomous incident response** is no longer future talk - it's deployed in production at large organizations. MTTD and MTTR are two critical metrics to track and continuously improve.
- **AI Agents don't replace engineers** - they free engineers from repetitive reactive work to focus on architectural improvements and strategy.
- **Multi-agent reasoning** is the right architecture for complex problems: each agent specializes in one task, combining to solve problems beyond the capability of any single agent.

#### On Voice AI and user experience
- Sub-500ms latency is a hard requirement for Voice Agents - failing to meet this threshold breaks the natural experience no matter how intelligent the AI is.
- **Speech-to-speech models** (like Amazon Nova Sonic) represent a significant leap - bypassing the text intermediate step reduces latency and preserves natural audio quality.

#### On security and enterprise architecture
- **MCP + VPC Private Connectivity** is the standard pattern for safely extending AI assistants in enterprise environments.
- Security must be designed from the start - not bolted on afterward. "Security by design" is not just a slogan; it's a practical requirement when AI accesses sensitive data.

---

### Personal Reflection

This workshop had a noticeably higher technical density than previous events - from Deep Response Engine architecture to configuring VPC private MCP connections, each session required a solid technical foundation to follow along.

What struck me most was the common thread running through all five sessions: **AI is no longer just for answering questions - it's for taking action**. Whether autonomously resolving incidents, processing voice conversations, planning workforces, or connecting enterprise systems - everything pointed toward AI that acts, not just responds.

That shift - from AI as a search engine to AI as an operator - is the real story of this event.

---

### Event Photos

![AWS First Cloud AI Journey Workshop](/images/event4.jpg)
