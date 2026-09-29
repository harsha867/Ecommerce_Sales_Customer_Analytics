from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
raw = DATA / "Online Retail.xlsx"
sample = DATA / "sample_retail_clean.csv"

# Load data: try Excel first, then sample CSV
if raw.exists():
    print("Loading from Online Retail.xlsx...")
    df = pd.read_excel(raw)
    df.columns = [c.strip() for c in df.columns]

    # Cleaning
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # Cancellation flag: UCI documents invoices beginning with C as cancellations.
    df["IsCancelled"] = df["InvoiceNo"].str.upper().str.startswith("C")

    # Keep valid sales for revenue/customer analysis.
    sales = df[
        (~df["IsCancelled"]) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0) &
        (df["CustomerID"].notna())
    ].copy()
elif sample.exists():
    print("Loading from sample_retail_clean.csv...")
    sales = pd.read_csv(sample)
    sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"], errors="coerce")
else:
    raise FileNotFoundError("No data found. Run python/download_data.py or use sample_retail_clean.csv")

sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]
sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

# Clean export
sales.to_csv(DATA / "retail_clean.csv", index=False)

# Monthly KPI
monthly = sales.groupby("YearMonth").agg(
    Revenue=("Revenue", "sum"),
    Orders=("InvoiceNo", "nunique"),
    Customers=("CustomerID", "nunique"),
    Units=("Quantity", "sum")
).reset_index()
monthly["Average_Order_Value"] = monthly["Revenue"] / monthly["Orders"]
monthly.to_csv(DATA / "monthly_sales.csv", index=False)

# Product analysis
products = sales.groupby(["StockCode", "Description"], dropna=False).agg(
    Revenue=("Revenue", "sum"),
    Units=("Quantity", "sum"),
    Orders=("InvoiceNo", "nunique")
).reset_index().sort_values("Revenue", ascending=False)
products.to_csv(DATA / "top_products.csv", index=False)

# Country analysis
country = sales.groupby("Country").agg(
    Revenue=("Revenue", "sum"),
    Orders=("InvoiceNo", "nunique"),
    Customers=("CustomerID", "nunique")
).reset_index().sort_values("Revenue", ascending=False)
country.to_csv(DATA / "country_sales.csv", index=False)

# RFM
snapshot = sales["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# Quintile scoring. rank(method='first') avoids duplicate qcut edges.
rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

def segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 4 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "Recent Customers"
    if r <= 2 and f >= 3:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Hibernating"
    return "Potential Loyalists"

rfm["Segment"] = rfm.apply(segment, axis=1)
rfm.to_csv(DATA / "customer_rfm.csv", index=False)

# Console summary
print("\n=== E-COMMERCE ANALYTICS SUMMARY ===")
print(f"Valid sales rows: {len(sales):,}")
print(f"Revenue: £{sales['Revenue'].sum():,.2f}")
print(f"Orders: {sales['InvoiceNo'].nunique():,}")
print(f"Customers: {sales['CustomerID'].nunique():,}")
print(f"Average order value: £{sales['Revenue'].sum()/sales['InvoiceNo'].nunique():,.2f}")
print("\nTop 5 products:")
print(products.head(5)[["Description", "Revenue"]].to_string(index=False))
print("\nRFM segments:")
print(rfm["Segment"].value_counts().to_string())
