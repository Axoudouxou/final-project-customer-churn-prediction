# Telco Customer Churn Prediction
## Data Science End-to-End Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-green.svg)](https://scikit-learn.org/)

---

##  Project Overview

This project develops a predictive model to identify telecom customers at risk of churning, enabling proactive retention strategies.

### Business Problem
- **27% annual churn rate** in the telecom industry
- High customer acquisition costs
- Need for data-driven retention strategies

### Objective
Build a machine learning model to:
- Predict customer churn with high accuracy
- Maximize **Recall** (minimize missed churners)
- Provide actionable business recommendations

---

##  Dataset

**Source:** Telco Customer Churn Dataset  
**Size:** 7,043 customers  
**Features:** 21 variables

### Feature Categories
- **Demographics:** Gender, Senior Citizen, Partner, Dependents
- **Services:** Phone, Internet, Online Security, Tech Support, Streaming
- **Contract:** Contract type, Tenure, Paperless billing
- **Billing:** Monthly charges, Total charges, Payment method

**Target Variable:** Churn (Yes/No)  
**Class Distribution:** 73% No Churn | 27% Churn (imbalanced)

---

##  Methodology

### 1. Data Exploration
- Missing value analysis (TotalCharges)
- Outlier detection
- Correlation analysis
- Churn rate by segment

### 2. Data Preparation
- One-hot encoding for categorical variables
- Train/Validation/Test split (60/20/20 stratified)
- Feature scaling with StandardScaler

### 3. Feature Engineering
- **VIF Analysis:** Removed multicollinearity (TotalCharges dropped)
- **New Feature:** `total_services` (count of active services)

### 4. Model Development

#### Phase 1: Initial Exploration
Tested 5 algorithms without class balancing:
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- K-Nearest Neighbors

**Result:** Low recall (48-53%) due to class imbalance

#### Phase 2: Class Balancing
Applied **SMOTE** (Synthetic Minority Over-sampling Technique)

**Result:** Massive improvement (+13-23 percentage points)

#### Phase 3: Systematic Comparison
Tested 4 configurations for top 2 models:
1. Baseline (default params, no balancing)
2. Hyperparameter tuning (GridSearchCV)
3. Tuned + SMOTE
4. Tuned + SMOTE + Threshold optimization

---

##  Results

### Champion Model
**Gradient Boosting + SMOTE**

| Metric | Score |
|--------|-------|
| **Recall** | **72.46%** |
| **F1-Score** | **61.24%** |
| Precision | 53.03% |
| ROC-AUC | 83.67% |
| Accuracy | 75.66% |

### Test Set Performance
- **Churners detected:** 271/374 (72.5%)
- **Churners missed:** 103 (27.5%)
- **Improvement vs baseline:** +88 customers saved (+23.5 points)

### Generalization
 **Excellent** - Test performance nearly identical to validation (F1 diff: 0.92%)

---

##  Key Insights

### Feature Importance (Top 5)
1. **Tenure (27.7%)** - Customer loyalty duration
2. **Contract Type (15.4%)** - Month-to-month vs annual
3. **Fiber Optic (13.8%)** - Service type
4. **Payment Method (12.5%)** - Electronic check risk
5. **Total Services (5.8%)** - Service engagement

### Critical Findings
- **Class balancing (SMOTE)** is t

## Author

**Carmelina M'BESSO**  
Junior Data Analyst - Specialized in CRM & Marketing Analytics  
[LinkedIn](https://linkedin.com/in/carmelina-axelle-mbesso)

---

## License

Academic Project - Ironhack 2026
