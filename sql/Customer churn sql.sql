CREATE DATABASE telco_churn
USE telco_churn

CREATE TABLE `customers_demographics` (
  `customer_id` VARCHAR(20) PRIMARY KEY,
  `gender` VARCHAR(10),
  `age` INT,
  `senior_citizen` VARCHAR(3),
  `married` VARCHAR(3),
  `dependents` VARCHAR(3),
  `number_of_dependents` INT
);

CREATE TABLE `customers_location` (
  `customer_id` VARCHAR(20) PRIMARY KEY,
  `country` VARCHAR(50),
  `state` VARCHAR(50),
  `city` VARCHAR(100),
  `zip_code` VARCHAR(10),
  `latitude` FLOAT,
  `longitude` FLOAT
);

CREATE TABLE `zip_population` (
  `zip_code` VARCHAR(10) PRIMARY KEY,
  `population` INT
);

CREATE TABLE `zip_census_data` (
  `zip_code` VARCHAR(10) PRIMARY KEY,
  `median_income` DECIMAL(10,2),
  `population_below_poverty` INT,
  `unemployed_population` INT
);

CREATE TABLE `customers_services` (
  `customer_id` VARCHAR(20) PRIMARY KEY,
  `quarter` VARCHAR(5),
  `tenure_in_months` INT,
  `phone_service` VARCHAR(3),
  `internet_service` VARCHAR(3),
  `internet_type` VARCHAR(20),
  `contract` VARCHAR(20),
  `payment_method` VARCHAR(50),
  `monthly_charge` DECIMAL(10,2),
  `total_charges` DECIMAL(10,2)
);

CREATE TABLE `customers_status` (
  `customer_id` VARCHAR(20) PRIMARY KEY,
  `satisfaction_score` INT,
  `churn_label` VARCHAR(3),
  `churn_value` INT,
  `churn_score` INT,
  `cltv` INT,
  `churn_category` VARCHAR(50),
  `churn_reason` VARCHAR(200)
);

ALTER TABLE `customers_location` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers_demographics` (`customer_id`);

ALTER TABLE `customers_location` ADD FOREIGN KEY (`zip_code`) REFERENCES `zip_population` (`zip_code`);

ALTER TABLE `zip_census_data` ADD FOREIGN KEY (`zip_code`) REFERENCES `zip_population` (`zip_code`);

ALTER TABLE `customers_services` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers_demographics` (`customer_id`);

ALTER TABLE `customers_status` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers_demographics` (`customer_id`);

SELECT * FROM customers_demographics;
SELECT * FROM zip_population;
SELECT * FROM customers_services;
SELECT * FROM customers_status;
SELECT * FROM zip_census_data;
SELECT * FROM customers_services;
SELECT * FROM customers_location;

SELECT COUNT(*) as count_demographics FROM customers_demographics;
SELECT COUNT(*) as count_location FROM customers_location;
SELECT COUNT(*) as count_services FROM customers_services;
SELECT COUNT(*) as count_status FROM customers_status;
SELECT COUNT(*) as count_zip_pop FROM zip_population;

-- WHICH CONTRACT CHURN THE MOST
SELECT 
    s.contract,
    COUNT(*) as total_customers,
    SUM(st.churn_value) as churned_customers,
    ROUND(AVG(st.churn_value) * 100, 2) as churn_rate_percent
FROM customers_services s
JOIN customers_status st ON s.customer_id = st.customer_id
GROUP BY s.contract
ORDER BY churn_rate_percent DESC;

-- DO CHURNED CUSTOMERS PAY HIGH PRICE OR NOT ?
SELECT 
    st.churn_label,
    COUNT(*) as customer_count,
    ROUND(AVG(s.monthly_charge), 2) as avg_monthly_charge,
    ROUND(MIN(s.monthly_charge), 2) as min_charge,
    ROUND(MAX(s.monthly_charge), 2) as max_charge
FROM customers_services s
JOIN customers_status st ON s.customer_id = st.customer_id
GROUP BY st.churn_label;

-- Top 10 Cities with Highest Churn Rate
SELECT 
    l.city,
    COUNT(*) as total_customers,
    SUM(st.churn_value) as churned_customers,
    ROUND(AVG(st.churn_value) * 100, 2) as churn_rate_percent
FROM customers_location l
JOIN customers_status st ON l.customer_id = st.customer_id
GROUP BY l.city
HAVING total_customers >= 50
ORDER BY churn_rate_percent DESC
LIMIT 10;

-- Senior Citizens Analysis
SELECT 
    d.senior_citizen,
    COUNT(*) as customer_count,
    ROUND(AVG(st.cltv), 2) as avg_cltv,
    ROUND(AVG(s.tenure_in_months), 2) as avg_tenure_months,
    ROUND(AVG(st.churn_value) * 100, 2) as churn_rate_percent
FROM customers_demographics d
JOIN customers_services s ON d.customer_id = s.customer_id
JOIN customers_status st ON d.customer_id = st.customer_id
GROUP BY d.senior_citizen;

-- Churn Reasons Distribution
SELECT 
    st.churn_category,
    COUNT(*) as churn_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers_status WHERE churn_value = 1), 2) as percentage
FROM customers_status st
WHERE st.churn_value = 1
GROUP BY st.churn_category
ORDER BY churn_count DESC;
