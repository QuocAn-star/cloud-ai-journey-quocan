---
title: "Step 5: EC2 & Dashboard"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5.4.5 </b> "
---

# Step 5: Deploy Streamlit Dashboard on EC2

In this step, you will launch an EC2 instance inside the VPC, install Python dependencies, deploy the `app_beautiful.py` Streamlit application, and access the live analytics dashboard.

**Estimated time:** 25–35 minutes

---

## Prerequisites

- Step 1 complete (VPC, subnet, security group `lakehouse-ec2-sg` created)
- Step 4 complete (Athena can query Gold tables)
- `app_beautiful.py` source file available

---

## 5.1 Create an IAM Role for EC2

The EC2 instance needs permissions to query Athena and read S3 results.

**AWS Console → IAM → Roles → Create role**

| Field | Value |
|-------|-------|
| Trusted entity type | AWS service |
| Service | EC2 |

**Add permissions:**
- `AmazonAthenaFullAccess` - to execute queries
- `AmazonS3ReadOnlyAccess` - to read Gold and athena-results

**Role name:** `lakehouse-ec2-role`

> ⚠️ **Least-privilege note:** In production, replace broad policies with a custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryResults",
        "athena:GetQueryExecution",
        "athena:StopQueryExecution",
        "athena:GetWorkGroup"
      ],
      "Resource": "arn:aws:athena:us-east-1:*:workgroup/lakehouse-wg"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket", "s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::customer-behavior-lakehouse1/gold/*",
        "arn:aws:s3:::customer-behavior-lakehouse1/athena-results/*",
        "arn:aws:s3:::customer-behavior-lakehouse1"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetDatabase",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 5.2 Launch EC2 Instance

**AWS Console → EC2 → Instances → Launch instances**

| Field | Value |
|-------|-------|
| Name | `lakehouse-dashboard` |
| AMI | Amazon Linux 2023 AMI (free tier eligible) |
| Instance type | `t3.micro` (Free Tier eligible) |
| Key pair | Create new: `lakehouse-key` → Download `.pem` file |
| VPC | `lakehouse-vpc` |
| Subnet | `lakehouse-public-subnet` |
| Auto-assign public IP | Enable |
| Security group | Select existing: `lakehouse-ec2-sg` |
| IAM instance profile | `lakehouse-ec2-role` |
| Storage | 8 GiB gp3 (default EBS) |

Click **Launch instance**.

> ⚠️ **Key pair warning:** Download and securely store the `.pem` file immediately. You cannot retrieve it after creation. Without it, you cannot SSH into the instance.

![EC2 Instance - lakehouse-dashboard running](/result/EC2/EC2%20Instance.jpg)

![EC2 Security Group - showing inbound rules for ports 22 and 8501](/result/EC2/Security%20Group.jpg)

---

## 5.3 Assign an Elastic IP (Recommended)

An Elastic IP ensures the dashboard URL doesn't change if the EC2 instance is stopped and restarted.

**AWS Console → EC2 → Elastic IPs → Allocate Elastic IP address**

- Click **Allocate** (default settings)

Then **Actions → Associate Elastic IP address**:
- Instance: select `lakehouse-dashboard`
- Click **Associate**

Note the Elastic IP address - this will be your dashboard URL: `http://<elastic-ip>:8501`

**CLI alternative:**
```bash
# Allocate Elastic IP
ALLOC_ID=$(aws ec2 allocate-address \
    --domain vpc \
    --query "AllocationId" --output text)

# Get your instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=lakehouse-dashboard" \
    --query "Reservations[0].Instances[0].InstanceId" --output text)

# Associate
aws ec2 associate-address \
    --instance-id $INSTANCE_ID \
    --allocation-id $ALLOC_ID
```

---

## 5.4 Connect to EC2 and Install Dependencies

SSH into the instance from your local machine:

```bash
# Set correct permissions on key file (Linux/Mac)
chmod 400 lakehouse-key.pem

# SSH into EC2 (replace <elastic-ip> with your actual IP)
ssh -i lakehouse-key.pem ec2-user@<elastic-ip>
```

Once connected, install Python dependencies:

```bash
# Update system packages
sudo dnf update -y

# Install Python pip
sudo dnf install python3-pip -y

# Install all required Python packages
pip3 install boto3 pandas streamlit plotly awswrangler pyathena

# Verify key packages installed correctly
python3 -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python3 -c "import awswrangler; print('AWS Wrangler:', awswrangler.__version__)"
python3 -c "import plotly; print('Plotly:', plotly.__version__)"
```

---

## 5.5 Deploy the Streamlit Application

**Option A: Transfer file via SCP (from local machine, second terminal)**

```bash
scp -i lakehouse-key.pem app_beautiful.py ec2-user@<elastic-ip>:~/app_beautiful.py
```

**Option B: Copy-paste on EC2 directly**

```bash
# On EC2: create the file and paste content
nano ~/app_beautiful.py
# Paste full content of app_beautiful.py, then Ctrl+X, Y, Enter
```

**Verify the configuration inside `app_beautiful.py`:**

The app contains these configuration variables - confirm they match your setup:

```python
DATABASE = "customer_behavior_catalog_db"         # Your Glue database
ATHENA_OUTPUT = "s3://customer-behavior-lakehouse1/athena-results/"  # Your results path
REGION = "us-east-1"                             # Your AWS region
```

If you used a different bucket name or database name in earlier steps, update these values.

---

## 5.6 Run the Dashboard

```bash
# Start Streamlit in background (continues after SSH closes)
nohup streamlit run app_beautiful.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    > ~/streamlit.log 2>&1 &

# Wait 3 seconds for startup
sleep 3

# Check startup logs
cat ~/streamlit.log
# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://0.0.0.0:8501

# Verify port 8501 is listening
ss -tlnp | grep 8501
```

**Access the dashboard:**

Open your browser and navigate to:
```
http://<elastic-ip>:8501
```

---

## 5.7 Dashboard Sections & Validation

The Streamlit app displays the following sections:

**KPI Cards (Top of dashboard):**
- Total Orders, Total Customers, Total Revenue ($), Avg Order Value, Total Events

**Interactive Charts:**

![Revenue Trend - area chart of daily revenue over time](/result/DashBoard/Revenue%20Trend.png)

![Top 10 Countries by Revenue - horizontal bar chart](/result/DashBoard/Top%2010%20Countries%20by%20Revenue.png)

![Revenue by Device - donut chart: mobile, desktop, tablet](/result/DashBoard/Revenue%20by%20Device.png)

![Revenue by Payment Method - bar chart](/result/DashBoard/Revenue%20by%20Payment%20Method.png)

![Revenue by Traffic Source - bar chart](/result/DashBoard/Revenue%20by%20Traffic%20Source.png)

![Event Distribution - bar chart by event type](/result/DashBoard/Event%20Distribution.png)

![Top Performers - 3-column comparison table](/result/DashBoard/Top%20Performers.jpg)

![View Daily Revenue Data - expandable data table](/result/DashBoard/View%20Daily%20Revenue%20Data.jpg)

---

**Validation checklist:**

| Dashboard Section | Expected Content | Validation |
|------------------|-----------------|------------|
| **KPI Cards** | 5 metrics, all numbers > 0 | Verify values are non-zero |
| **Revenue Trend** | Area chart with dates on x-axis | Dates visible, revenue in $ |
| **Event Distribution** | At least 3–5 event types | Bars rendered correctly |
| **Top 10 Countries** | Countries sorted by revenue | Correct descending order |
| **Revenue by Device** | Donut with 3 slices | mobile, desktop, tablet |
| **Revenue by Payment** | Bar with 3 bars | credit_card, paypal, bank_transfer |
| **Revenue by Source** | Bar with 4 bars | organic, social, email, paid_ads |
| **Top Performers** | 3-column table | Top 5 per category |
| **Daily Revenue Data** | Expandable table | Full date-sorted data |

---

## 5.8 Keep Dashboard Running Persistently

To ensure the dashboard continues running after you close the SSH session, use a systemd service:

```bash
# Create systemd service file
sudo tee /etc/systemd/system/streamlit.service << EOF
[Unit]
Description=Streamlit Lakehouse Dashboard
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user
ExecStart=/usr/local/bin/streamlit run /home/ec2-user/app_beautiful.py \
    --server.port 8501 \
    --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit
```

**Useful management commands:**

```bash
# View live dashboard logs
tail -f ~/streamlit.log

# Check running process
ps aux | grep streamlit

# Stop the dashboard
pkill -f streamlit
# or
sudo systemctl stop streamlit

# Restart after code update
sudo systemctl restart streamlit
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Connection refused` on port 8501 | Streamlit not started or crashed | Check `cat ~/streamlit.log` for errors |
| `Browser can't connect` | Security Group missing port 8501 rule | Add inbound Custom TCP rule for 8501 |
| `AccessDeniedException` in dashboard | EC2 IAM role missing Athena/S3 permissions | Check `lakehouse-ec2-role` has correct policies |
| `No module named 'awswrangler'` | Package not installed | Run `pip3 install awswrangler` on EC2 |
| Dashboard shows 0 for all metrics | Athena tables empty | Re-run silver-to-gold-job (Step 3) |
| SSH connection refused | EC2 not running or Security Group missing port 22 | Check EC2 state in Console, verify SG rules |

✅ **Step 5 complete** - Proceed to [Step 6: Monitoring with CloudWatch](../5.4.6-Monitoring/)
