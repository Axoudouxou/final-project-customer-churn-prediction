SELECT 
  CASE 
    WHEN `Tenure in Months` BETWEEN 0 AND 12 THEN '0-12 months'
    WHEN `Tenure in Months` BETWEEN 13 AND 24 THEN '13-24 months'
    WHEN `Tenure in Months` BETWEEN 25 AND 36 THEN '25-36 months'
    WHEN `Tenure in Months` BETWEEN 37 AND 48 THEN '37-48 months'
    ELSE '48+ months'
  END as tenure_bucket,
  COUNT(*) as total_customers,
  SUM(`Churn Value`) as churned,
  ROUND(AVG(`Churn Value`) * 100, 2) as churn_rate_pct,
  -- Cumulative churn (window function)
  SUM(SUM(`Churn Value`)) OVER (ORDER BY MIN(`Tenure in Months`)) as cumulative_churn
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
GROUP BY tenure_bucket
ORDER BY MIN(`Tenure in Months`);