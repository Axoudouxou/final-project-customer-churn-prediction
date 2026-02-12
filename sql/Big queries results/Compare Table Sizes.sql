SELECT 
  table_id as table_name,
  ROUND(size_bytes / (1024*1024), 2) as size_mb,
  row_count
FROM `telco-churn-analysis-486921.telco_churn_analysis.__TABLES__`
WHERE table_id IN ('Customers', 'Customers_optimized');