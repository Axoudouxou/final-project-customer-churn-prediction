SELECT 
  `Internet Type`,
  Contract,
  COUNT(*) as total_customers,
  SUM(`Churn Value`) as churned,
  ROUND(AVG(`Churn Value`) * 100, 2) as churn_rate_pct,
  ROUND(AVG(`Monthly Charge`), 2) as avg_monthly_charge,
  ROUND(AVG(CLTV), 2) as avg_cltv,
  -- Rank by revenue impact
  RANK() OVER (ORDER BY SUM(CASE WHEN `Churn Value` = 1 THEN CLTV ELSE 0 END) DESC) as revenue_risk_rank
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
WHERE `Internet Type` IS NOT NULL
GROUP BY `Internet Type`, Contract
ORDER BY churn_rate_pct DESC;