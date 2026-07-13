import boto3
import pandas as pd
import streamlit as st
import plotly.express as px
import awswrangler as wr

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Customer Behavior Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main {
    background-color:#f6f8fb;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

div[data-testid="metric-container"]{
    background:white;
    border:1px solid #E5E7EB;
    padding:15px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

h1,h2,h3{
    color:#1F2937;
}

hr{
    margin-top:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# AWS / ATHENA CONFIG
# ==========================================================
DATABASE = "customer_behavior_catalog_db"
ATHENA_OUTPUT = "s3://customer-behavior-lakehouse1/athena-results/"
REGION = "us-east-1"

boto3_session = boto3.Session(region_name=REGION)

# ==========================================================
# LOAD DATA FROM ATHENA
# ==========================================================
@st.cache_data(ttl=600)
def load_table(table_name: str) -> pd.DataFrame:
    return wr.athena.read_sql_query(
        sql=f"SELECT * FROM {table_name}",
        database=DATABASE,
        s3_output=ATHENA_OUTPUT,
        boto3_session=boto3_session,
        ctas_approach=False
    )


summary = load_table("dashboard_summary")
daily_revenue = load_table("daily_revenue")
event_summary = load_table("event_summary")
country_revenue = load_table("country_revenue")
device_summary = load_table("device_summary")
payment_summary = load_table("payment_summary")
source_summary = load_table("source_summary")

daily_revenue["order_date"] = pd.to_datetime(daily_revenue["order_date"])

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("Dashboard")

    st.markdown("---")

    st.success("Customer Behavior Analytics")

    st.write("Data Layer")

    st.info("Gold Layer")

    st.markdown("---")

    st.subheader("Dataset")

    st.write(f"Revenue Records : {len(daily_revenue):,}")

    st.write(f"Countries : {len(country_revenue):,}")

    st.write(f"Devices : {len(device_summary):,}")

    st.write(f"Payments : {len(payment_summary):,}")

    st.write(f"Traffic Sources : {len(source_summary):,}")

    st.markdown("---")



# ==========================================================
# HEADER
# ==========================================================

st.title("Customer Behavior Analytics Dashboard")

st.caption(
"Interactive Business Intelligence Dashboard "
    "built on Gold Layer"
)

# ==========================================================
# KPI
# ==========================================================

s = summary.iloc[0]

col1,col2,col3,col4,col5 = st.columns(5)

with col1:

    st.metric(
        "Orders",
        f"{int(s['total_orders']):,}"
    )

with col2:

    st.metric(
        "Customers",
        f"{int(s['total_customers']):,}"
    )

with col3:

    st.metric(
        "Revenue",
        f"${s['total_revenue']:,.0f}"
    )

with col4:

    st.metric(
        "Avg Order",
        f"${s['avg_order_value']:,.2f}"
    )

with col5:

    st.metric(
        "Events",
        f"{int(s['total_events']):,}"
    )

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

top_country = country_revenue.sort_values(
    "total_revenue",
    ascending=False
).iloc[0]

top_device = device_summary.sort_values(
    "total_revenue",
    ascending=False
).iloc[0]

top_payment = payment_summary.sort_values(
    "total_revenue",
    ascending=False
).iloc[0]

top_source = source_summary.sort_values(
    "total_revenue",
    ascending=False
).iloc[0]

st.markdown("## Executive Summary")

left,right = st.columns([3,2])

with left:

    st.success(f"""

### Business Highlights

- Total Revenue reached **${s['total_revenue']:,.0f}**

- Highest Revenue Country : **{top_country['country']}**

- Best Performing Device : **{top_device['device']}**

- Top Payment Method : **{top_payment['payment_method']}**

- Best Traffic Source : **{top_source['source']}**

""")

with right:

    st.info(f"""

### Quick Facts

- Orders: **{int(s['total_orders']):,}**

- Customers: **{int(s['total_customers']):,}**

- Events: **{int(s['total_events']):,}**

""")

st.divider()

# ==========================================================
# REVENUE TREND
# ==========================================================

st.subheader("Revenue Trend")

fig_daily = px.area(
    daily_revenue,
    x="order_date",
    y="total_revenue",
    template="plotly_white",
    color_discrete_sequence=["#2563EB"]
)

fig_daily.update_traces(
    opacity=0.8
)

fig_daily.update_layout(
    height=460,
    title="Daily Revenue",
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Revenue ($)",
    xaxis=dict(
        tickformat="%Y"
    ),
    yaxis=dict(
        tickprefix="$",
        separatethousands=True
    )
)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)

peak = daily_revenue.loc[
    daily_revenue["total_revenue"].idxmax()
]

st.info(
    f"""
**Insight**

- Highest revenue occurred on **{peak['order_date'].strftime('%d %b %Y')}**

- Revenue reached **${peak['total_revenue']:,.0f}**
"""
)

st.divider()
# ==========================================================
# EVENT SUMMARY & COUNTRY REVENUE
# ==========================================================

col_left, col_right = st.columns(2)

# ----------------------------------------------------------
# EVENT SUMMARY
# ----------------------------------------------------------

with col_left:

    st.subheader("Event Distribution")

    event_col = (
        "event_type"
        if "event_type" in event_summary.columns
        else "event"
    )

    event_summary = event_summary.sort_values(
        "total_events",
        ascending=False
    )

    fig_event = px.bar(
        event_summary,
        x=event_col,
        y="total_events",
        color="total_events",
        color_continuous_scale="Blues",
        template="plotly_white",
        text_auto=True
    )

    fig_event.update_layout(

        height=420,

        xaxis_title="Event",

        yaxis_title="Total Events",

        coloraxis_showscale=False

    )

    st.plotly_chart(
        fig_event,
        use_container_width=True
    )

    top_event = event_summary.iloc[0]

    percent = (
        top_event["total_events"]
        / event_summary["total_events"].sum()
        * 100
    )

    st.info(
        f"""
**Insight**

- **{top_event[event_col]}** is the most frequent customer activity.

- It accounts for **{percent:.1f}%** of all recorded events.
"""
    )

# ----------------------------------------------------------
# COUNTRY REVENUE
# ----------------------------------------------------------

with col_right:

    st.subheader("Top 10 Countries by Revenue")

    country_top = country_revenue.sort_values(
        "total_revenue",
        ascending=False
    ).head(10)

    fig_country = px.bar(

        country_top,

        y="country",

        x="total_revenue",

        orientation="h",

        color="total_revenue",

        color_continuous_scale="Viridis",

        template="plotly_white",

        text_auto=".2s"

    )

    fig_country.update_layout(

        height=420,

        xaxis_title="Revenue ($)",

        yaxis_title="",

        coloraxis_showscale=False

    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

    top_country = country_top.iloc[0]

    country_percent = (
        top_country["total_revenue"]
        / country_revenue["total_revenue"].sum()
        * 100
    )

    st.success(
        f"""
**Insight**

- **{top_country['country']}** generated the highest revenue.

- Contribution: **{country_percent:.1f}%** of total revenue.
"""
    )

st.divider()

# ==========================================================
# DEVICE & PAYMENT
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# DEVICE
# ----------------------------------------------------------

with left:

    st.subheader("Revenue by Device")

    fig_device = px.pie(
device_summary,

        names="device",

        values="total_revenue",

        hole=0.60,

        template="plotly_white"

    )

    fig_device.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    fig_device.update_layout(

        height=420

    )

    st.plotly_chart(

        fig_device,

        use_container_width=True

    )

    top_device = device_summary.sort_values(
        "total_revenue",
        ascending=False
    ).iloc[0]

    device_percent = (
        top_device["total_revenue"]
        / device_summary["total_revenue"].sum()
        * 100
    )

    st.info(
        f"""
**Insight**

- Most revenue comes from **{top_device['device']}**

- Contribution: **{device_percent:.1f}%**
"""
    )

# ----------------------------------------------------------
# PAYMENT
# ----------------------------------------------------------

with right:

    st.subheader("Revenue by Payment Method")

    payment_sorted = payment_summary.sort_values(
        "total_revenue",
        ascending=False
    )

    fig_payment = px.bar(

        payment_sorted,

        x="payment_method",

        y="total_revenue",

        color="total_revenue",

        color_continuous_scale="Greens",

        template="plotly_white",

        text_auto=".2s"

    )

    fig_payment.update_layout(

        height=420,

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Revenue ($)"

    )

    st.plotly_chart(

        fig_payment,

        use_container_width=True

    )

    top_payment = payment_sorted.iloc[0]

    payment_percent = (
        top_payment["total_revenue"]
        / payment_summary["total_revenue"].sum()
        * 100
    )

    st.success(
        f"""
**Insight**

- Customers mostly use **{top_payment['payment_method']}**

- It contributes **{payment_percent:.1f}%** of total revenue.
"""
    )

st.divider()
# ==========================================================
# TRAFFIC SOURCE
# ==========================================================

st.subheader("Revenue by Traffic Source")

source_sorted = source_summary.sort_values(
    "total_revenue",
    ascending=False
)

fig_source = px.bar(

    source_sorted,

    x="source",

    y="total_revenue",

    color="total_revenue",

    color_continuous_scale="Oranges",

    template="plotly_white",

    text_auto=".2s"

)

fig_source.update_layout(

    height=450,

    coloraxis_showscale=False,

    xaxis_title="Traffic Source",

    yaxis_title="Revenue ($)"

)

st.plotly_chart(
    fig_source,
    use_container_width=True
)

top_source = source_sorted.iloc[0]

source_percent = (
    top_source["total_revenue"]
    / source_summary["total_revenue"].sum()
    * 100
)

st.info(
f"""
**Insight**

- The highest revenue comes from **{top_source['source']}**.

- Contribution: **{source_percent:.1f}%** of total revenue.
"""
)

st.divider()

# ==========================================================
# TOP RANKINGS
# ==========================================================

st.subheader("Top Performers")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### Top Countries")

    country_rank = (
        country_revenue
        .sort_values("total_revenue", ascending=False)
        .head(5)
        [["country", "total_revenue"]]
        .reset_index(drop=True)
    )

    st.dataframe(
        country_rank,
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.markdown("### Top Devices")

    device_rank = (
        device_summary
        .sort_values("total_revenue", ascending=False)
        .head(5)
        [["device", "total_revenue"]]
        .reset_index(drop=True)
    )

    st.dataframe(
        device_rank,
        use_container_width=True,
        hide_index=True
    )

with col3:

    st.markdown("### Top Sources")

    source_rank = (
        source_summary
        .sort_values("total_revenue", ascending=False)
        .head(5)
        [["source", "total_revenue"]]
        .reset_index(drop=True)
    )

    st.dataframe(
        source_rank,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================================
# DATA PREVIEW
# ==========================================================

with st.expander("View Daily Revenue Data"):

    st.dataframe(
        daily_revenue.sort_values(
            "order_date",
            ascending=False
        ),
        use_container_width=True
    )

st.divider()

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.subheader("Dashboard Summary")

summary_text = f"""

### Key Findings

- Total Revenue reached **${s['total_revenue']:,.0f}**

- Total Orders: **{int(s['total_orders']):,}**
- Total Customers: **{int(s['total_customers']):,}**

- Average Order Value: **${s['avg_order_value']:,.2f}**

- Highest Revenue Country: **{top_country['country']}**

- Best Device: **{top_device['device']}**

- Preferred Payment Method: **{top_payment['payment_method']}**

- Best Traffic Source: **{top_source['source']}**

These insights indicate where the business is generating the most value and can support future marketing and operational decisions.

"""

st.success(summary_text)

st.divider()
