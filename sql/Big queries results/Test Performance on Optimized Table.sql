SELECT 
    Contract,
    COUNT(*) as total_customers,
    SUM(`Churn Value`) as churned,
    ROUND(AVG(`Churn Value`) * 100, 2) as churn_rate_pct,
    ROUND(AVG(`Monthly Charge`), 2) as avg_monthly_charge
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
WHERE DATE(created_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
GROUP BY Contract
ORDER BY churn_rate_pct DESC;