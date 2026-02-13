# Customer Telco Churn Prediction

Machine Learning-powered retention strategy for California telecommunications company.

## Project Overview

**Goal:** Predict customer churn with 70%+ recall to enable proactive retention campaigns

**Results:** 
- 72.46% Recall achieved (271 of 374 churners detected)
- $924K annual revenue protection
- 15.1% ROI on retention campaigns

**Tech Stack:** Python, MySQL, BigQuery, Flask, Tableau, scikit-learn

---

## Table of Contents

1. [Data Collection](#data-collection)
2. [Data Pipeline](#data-pipeline)
3. [Database Architecture](#database-architecture)
4. [Machine Learning](#machine-learning)
5. [API Deployment](#api-deployment)
6. [Results](#results)
7. [Installation](#installation)

---

## Data Collection

Multi-source data pipeline :

| Source | Type | Records | Purpose |
|--------|------|---------|---------|
| IBM Telco Dataset | CSV | 7,043 | Customer profiles |
| US Census Bureau API | REST | 1,627 | Economic context |
| Web Scraping (Wikipedia, FCC) | HTML | 1,057 | Competitive intelligence |
| MySQL Database | RDBMS | 7,043 | Normalized storage |
| Google BigQuery | Big Data | 7,043 | Advanced analytics |

---

## Data Pipeline
```
CSV/API/Scraping → Python ETL → Data Cleaning → Feature Engineering
                                      ↓
                              MySQL (6 tables, 3NF)
                                      ↓
                              BigQuery (partitioned/clustered)
                                      ↓
                              ML Model Training
                                      ↓
                              Flask REST API
```

---

## Database Architecture

**MySQL Database (3NF Normalized):**

- `customers_demographics` (7,043 rows)
- `customers_location` (7,043 rows)
- `customers_services` (7,043 rows)
- `customers_status` (7,043 rows)
- `zip_census_data` (1,627 rows)
- `zip_population` (1,627 rows)

**BigQuery Optimization:**
- Partitioned by: `DATE(created_timestamp)`
- Clustered by: `Contract`, `Churn Label`, `Internet Type`
- Performance: 3.5× faster queries, 65% less data scanned

See: [SQL Scripts](./sql/)
Big query :[BIG QUERY](https://console.cloud.google.com/bigquery?organizationId=0&project=telco-churn-analysis-486921&ws=!1m5!1m4!16m3!1m1!1stelco-churn-analysis-486921!3e12)

---

## Machine Learning

**Algorithm:** Gradient Boosting + SMOTE

**Performance (Test Set):**
- Recall: 72.46%
- Precision: 53.03%
- F1-Score: 61.24%
- ROC-AUC: 83.67%

**Why Recall?** Missing a churner costs $3,456 (lost CLTV) vs $150 for false alarm. Cost ratio: 23:1

**Feature Importance:**
1. Contract type (51.1%)
2. Tenure (18.4%)
3. Monthly charges (12.7%)

See: [Notebooks](./notebooks/)

---

## API Deployment

**RESTful API with Flask**

Endpoints:
- `GET /api/customers` - Paginated customer list with filters
- `GET /api/customers/{id}` - Single customer profile (6-table JOIN)
- `GET /api/predictions` - Historical predictions
- `POST /api/predictions` - Real-time churn prediction
- `GET /health` - Service health check

**Run locally:**
```bash
cd api
pip install -r requirements.txt
python app.py
```

Access at: `http://localhost:5001`

See: [API Documentation](./api/)

---

## Results

**Business Impact:**
- Annual revenue protection: $924,358
- Campaign ROI: 15.1%
- API response time: <1 second

**Visualizations:**
- [Tableau Dashboard](https://public.tableau.com/app/profile/carmelina.mbesso/viz/Classeur1_17708052695380/STORY)

---

## Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Node.js (for BigQuery queries)

### Setup
```bash
# Clone repository
git clone https://github.com/Axoudouxou/final-project-customer-churn-prediction.git
cd final-project-customer-churn-prediction

# Install dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < sql/create_database.sql

# Run API
cd api
python app.py
```

---

## Project Structure
```
├── data/               # Raw and processed datasets
├── notebooks/          # Jupyter notebooks (EDA, modeling)
├── sql/                # MySQL and BigQuery queries
├── api/                # Flask REST API
├── docs/               # Documentation and reports
└── presentation/       # PowerPoint presentation
```

---

## Documentation

- [RNCP Report](./docs/Dossier%20RNCP%20Carmelina%20Mbesso.pdf)
- [Data Dictionary](./docs/Telco_Data_Dictionary.pdf)
- [Presentation Slides](./docs/CUSTOMER%20CHURN%20PREDICTION.pdf)
- [ERD Diagram](./docs/ERD_diagram.png)

---

## Technologies Used

**Languages:** Python, SQL

**Libraries:** 
- Data: pandas, numpy, scikit-learn
- ML: XGBoost, imbalanced-learn (SMOTE)
- Visualization: matplotlib, seaborn, Tableau
- API: Flask, mysql-connector-python

**Infrastructure:**
- Database: MySQL 8.0
- Big Data: Google BigQuery
- Version Control: Git/GitHub

---

## Author

**Carmelina M'BESSO**

Data Analytics Bootcamp - Ironhack  
RNCP Level 6 Certification

- LinkedIn: [linkedin.com/in/carmelinambesso](https://www.linkedin.com/in/carmelina-axelle-mbesso-1640b5205/)
- Email: axmbesso.am@gmail.com

---

## License

This project was developed as part of the RNCP Data Analytics certification (February 2026).