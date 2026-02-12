SELECT 
  City,
  State,
  COUNT(*) as total_customers,
  SUM(`Churn Value`) as churned_count,
  ROUND(AVG(`Churn Value`) * 100, 2) as churn_rate_pct,
  ROUND(AVG(`Monthly Charge`), 2) as avg_monthly_charge,
  -- Percentiles (BigQuery-specific function)
  APPROX_QUANTILES(`Monthly Charge`, 4)[OFFSET(2)] as median_monthly_charge,
  ROUND(STDDEV(`Monthly Charge`), 2) as stddev_monthly_charge
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
GROUP BY City, State
HAVING total_customers >= 30
ORDER BY churned_count DESC
LIMIT 15;