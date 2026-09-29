# Project 1 — E-Commerce Sales & Customer Analytics

## Business goal
Analyze online retail transactions to understand revenue trends, product performance,
customer value, geography, cancellations, and repeat-purchase behavior.

## Dataset
Official source: UCI Online Retail.
The full dataset contains 541,909 transactions from a UK-based online retailer
between 01-Dec-2010 and 09-Dec-2011.

Download through Python:
    pip install ucimlrepo
    python python/download_data.py

Or download manually from the official UCI page.

## Skills demonstrated
Python, Pandas, NumPy, SQL, data cleaning, EDA, RFM analysis, customer segmentation,
KPI design, Power BI, DAX, business storytelling.

## Folder structure
data/       raw and cleaned data
python/     download + cleaning + analysis
sql/        SQL schema and business questions
powerbi/    DAX measures and dashboard plan

## Run
pip install -r requirements.txt
python python/download_data.py
python python/analysis.py

The analysis script creates:
data/retail_clean.csv
data/monthly_sales.csv
data/top_products.csv
data/customer_rfm.csv
data/country_sales.csv

## Suggested Power BI pages
1. Executive Sales Overview
2. Product Performance
3. Customer/RFM Segmentation
4. Geography & Trends

## Resume bullet
Built an end-to-end e-commerce analytics solution using Python, SQL and Power BI,
cleaning 541K+ transactions, analyzing revenue/product/customer trends, and creating
RFM-based customer segments and KPI dashboards.
