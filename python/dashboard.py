import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Load all analysis outputs
retail = pd.read_csv(DATA / "retail_clean.csv")
monthly = pd.read_csv(DATA / "monthly_sales.csv")
products = pd.read_csv(DATA / "top_products.csv")
country = pd.read_csv(DATA / "country_sales.csv")
rfm = pd.read_csv(DATA / "customer_rfm.csv")

# Create dashboard with subplots
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Revenue by Month", "Top 10 Products",
        "Revenue by Country", "RFM Segments",
        "Orders Trend", "Average Order Value Trend"
    ),
    specs=[
        [{"secondary_y": False}, {"secondary_y": False}],
        [{"secondary_y": False}, {"type": "domain"}],
        [{"secondary_y": False}, {"secondary_y": False}]
    ]
)

# 1. Revenue by Month (Line chart)
fig.add_trace(
    go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#636EFA", width=2)
    ),
    row=1, col=1
)

# 2. Top 10 Products (Bar chart)
top10 = products.head(10)
fig.add_trace(
    go.Bar(
        x=top10["Revenue"],
        y=top10["Description"],
        orientation="h",
        name="Product Revenue",
        marker=dict(color="#EF553B")
    ),
    row=1, col=2
)

# 3. Revenue by Country (Top 10)
top_countries = country.head(10)
fig.add_trace(
    go.Bar(
        x=top_countries["Country"],
        y=top_countries["Revenue"],
        name="Country Revenue",
        marker=dict(color="#00CC96")
    ),
    row=2, col=1
)

# 4. RFM Segments (Pie chart)
segment_counts = rfm["Segment"].value_counts()
fig.add_trace(
    go.Pie(
        labels=segment_counts.index,
        values=segment_counts.values,
        name="Segments",
        marker=dict(colors=["#AB63FA", "#FFA15A", "#00CC96", "#EF553B", "#636EFA", "#AB63FA"])
    ),
    row=2, col=2
)

# 5. Orders Trend (Line chart)
fig.add_trace(
    go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Orders"],
        mode="lines+markers",
        name="Orders",
        line=dict(color="#00CC96", width=2)
    ),
    row=3, col=1
)

# 6. Average Order Value Trend (Line chart)
fig.add_trace(
    go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Average_Order_Value"],
        mode="lines+markers",
        name="AOV",
        line=dict(color="#FFA15A", width=2)
    ),
    row=3, col=2
)

# Update axes labels
fig.update_xaxes(title_text="Month", row=1, col=1)
fig.update_yaxes(title_text="Revenue (£)", row=1, col=1)

fig.update_xaxes(title_text="Revenue (£)", row=1, col=2)
fig.update_yaxes(title_text="Product", row=1, col=2)

fig.update_xaxes(title_text="Country", row=2, col=1)
fig.update_yaxes(title_text="Revenue (£)", row=2, col=1)

fig.update_xaxes(title_text="Month", row=3, col=1)
fig.update_yaxes(title_text="Orders", row=3, col=1)

fig.update_xaxes(title_text="Month", row=3, col=2)
fig.update_yaxes(title_text="AOV (£)", row=3, col=2)

# Update layout
fig.update_layout(
    height=1200,
    width=1400,
    title_text="E-Commerce Sales & Customer Analytics Dashboard",
    showlegend=False,
    template="plotly_white"
)

# Save dashboard
dashboard_path = ROOT / "dashboard.html"
fig.write_html(str(dashboard_path))
print(f"✓ Dashboard created: {dashboard_path}")

# Create KPI summary card
kpi_fig = go.Figure()

total_revenue = retail["Revenue"].sum()
total_orders = retail["InvoiceNo"].nunique()
total_customers = retail["CustomerID"].nunique()
avg_order_value = total_revenue / total_orders

kpi_text = f"""
<b>E-COMMERCE ANALYTICS KPIs</b><br>
━━━━━━━━━━━━━━━━━━━━━━━━━<br>
Total Revenue: £{total_revenue:,.2f}<br>
Total Orders: {total_orders:,}<br>
Total Customers: {total_customers:,}<br>
Avg Order Value: £{avg_order_value:,.2f}<br>
<br>
Top Product: {products.iloc[0]['Description']}<br>
Top Country: {country.iloc[0]['Country']}<br>
<br>
<b>Customer Segments:</b><br>
Champions: {len(rfm[rfm['Segment'] == 'Champions'])}<br>
Loyal Customers: {len(rfm[rfm['Segment'] == 'Loyal Customers'])}<br>
At Risk: {len(rfm[rfm['Segment'] == 'At Risk'])}<br>
"""

kpi_fig.add_annotation(
    text=kpi_text,
    xref="paper", yref="paper",
    x=0.5, y=0.5,
    showarrow=False,
    font=dict(size=14, family="Courier New"),
    bgcolor="lightblue",
    bordercolor="navy",
    borderwidth=2,
    borderpad=20
)

kpi_fig.update_layout(
    height=400,
    width=600,
    title="KPI Summary",
    template="plotly_white",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

kpi_path = ROOT / "kpi_summary.html"
kpi_fig.write_html(str(kpi_path))
print(f"✓ KPI Summary created: {kpi_path}")

print("\n✓ Dashboard files created successfully!")
print(f"   Open in browser: {dashboard_path}")
