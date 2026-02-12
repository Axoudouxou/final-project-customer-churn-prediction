SELECT 
  Contract,
  `Churn Category`,
  COUNT(*) as churn_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Contract), 2) as pct_within_contract,
  ARRAY_AGG(DISTINCT `Churn Reason` IGNORE NULLS LIMIT 3) as top_3_reasons,
  ROUND(AVG(CLTV), 2) as avg_cltv_lost
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
WHERE `Churn Label` = true
  AND `Churn Category` IS NOT NULL
GROUP BY Contract, `Churn Category`
HAVING churn_count >= 5
ORDER BY Contract, churn_count DESC;