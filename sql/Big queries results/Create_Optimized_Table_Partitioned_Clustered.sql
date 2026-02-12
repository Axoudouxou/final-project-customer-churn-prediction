SELECT  FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers` LIMIT 1000

CREATE OR REPLACE TABLE `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
PARTITION BY DATE(created_timestamp)
CLUSTER BY Contract, `Churn Label`, `Internet Type`
AS 
SELECT 
  *,
  CURRENT_TIMESTAMP() as created_timestamp
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers`;