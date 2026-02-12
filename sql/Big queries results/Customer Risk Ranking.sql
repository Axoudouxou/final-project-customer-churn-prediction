SELECT 
    `Customer ID`,
    Contract,
    `Churn Score`,
    `Monthly Charge`,
    `Tenure in Months`,
    ROW_NUMBER() OVER (PARTITION BY Contract ORDER BY `Churn Score` DESC) as risk_rank
FROM `telco-churn-analysis-486921.telco_churn_analysis.Customers_optimized`
WHERE `Churn Score` IS NOT NULL
QUALIFY risk_rank <= 10
ORDER BY Contract, risk_rank;