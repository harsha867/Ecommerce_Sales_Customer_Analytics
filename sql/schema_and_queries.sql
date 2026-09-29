-- MySQL 8+ example
CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

CREATE TABLE retail_clean (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(30),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(12,2),
    CustomerID INT,
    Country VARCHAR(100),
    IsCancelled BOOLEAN,
    Revenue DECIMAL(14,2)
);

-- Load retail_clean.csv using your SQL client/import wizard.

-- 1. Monthly revenue
SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
       ROUND(SUM(Revenue),2) AS revenue,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM retail_clean
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY month;

-- 2. Top products by revenue
SELECT StockCode, Description,
       ROUND(SUM(Revenue),2) AS revenue,
       SUM(Quantity) AS units
FROM retail_clean
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 10;

-- 3. Country performance
SELECT Country,
       ROUND(SUM(Revenue),2) AS revenue,
       COUNT(DISTINCT CustomerID) AS customers,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM retail_clean
GROUP BY Country
ORDER BY revenue DESC;

-- 4. Repeat customers
WITH customer_orders AS (
    SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS orders
    FROM retail_clean
    GROUP BY CustomerID
)
SELECT
    SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
    COUNT(*) AS total_customers,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_pct
FROM customer_orders;
