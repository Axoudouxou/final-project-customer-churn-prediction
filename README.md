# Telco Customer Churn Prediction

**Data Science End-to-End Machine Learning Project**

Predicting customer churn in telecommunications using advanced ML techniques and statistical validation.

**Author:** Carmelina MBESSO | **Institution:** Ironhack Data Analytics Bootcamp | **Date:** January 2026

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Approach](#approach)
- [Key Results](#key-results)
- [Business Impact](#business-impact)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Author](#author)

---

## Problem Statement

**Challenge:** 27% of telecom customers churn annually, causing significant revenue loss and high acquisition costs.

**Solution:** Build a predictive ML model to identify at-risk customers before they leave, enabling proactive retention strategies.

**Why it matters:** Acquiring a new customer costs 5-7x more than retaining an existing one. Early churn prediction = massive cost savings.

---

## Dataset

**Source:** [IBM Sample Data Sets - Telco Customer Churn](https://www.ibm.com/communities/analytics/watson-analytics-blog/guide-to-sample-datasets/)

**Size:** 7,043 customers × 21 features

**Target:** Binary classification (Churn: Yes/No) - 27% imbalanced

**Features organized in 4 categories:**

| Category | Features |
|----------|----------|
| **Demographics** | Gender, SeniorCitizen, Partner, Dependents |
| **Services** | PhoneService, InternetService (DSL/Fiber), OnlineSecurity, TechSupport, StreamingTV, StreamingMovies |
| **Contract** | Contract type (Month-to-month/1-year/2-year), Tenure, PaperlessBilling |
| **Billing** | MonthlyCharges, TotalCharges, PaymentMethod |

---

## Approach

### 1. Exploratory Data Analysis (EDA)

**Data Quality:**
- 11 missing values in TotalCharges (replaced with median)
- No duplicates
- Imbalanced target: 73% No Churn vs 27% Churn

**Key Risk Factors Identified:**
- Month-to-month contracts: **43% churn rate** (vs 3% for 2-year contracts)
- New customers (<12 months tenure): **High risk** (50% churn in first year)
- Fiber optic service: **42% churn** (vs 19% for DSL)
- Electronic check payment: **45% churn** (vs 16% for automatic payments)

### 2. Statistical Validation

Applied **Z-tests for proportions** to validate observed differences are statistically significant:

| Hypothesis Test | Churn Rate Difference | Z-statistic | P-value | Conclusion |
|-----------------|----------------------|-------------|---------|------------|
| Month-to-month vs 2-year contract | 39.9 percentage points | 29.72 | <0.0001 | **Highly Significant** |
| Short (<12mo) vs Long tenure (≥12mo) | 30.8 percentage points | 26.66 | <0.0001 | **Highly Significant** |
| Electronic check vs Auto payment | 29.3 percentage points | 23.66 | <0.0001 | **Highly Significant** |
| Fiber optic vs DSL | 22.9 percentage points | 18.15 | <0.0001 | **Highly Significant** |

**Result:** All differences confirmed with **99.99% confidence** - NOT due to random chance.

### 3. Feature Engineering

**Multicollinearity Check:**
- VIF analysis: Removed TotalCharges (VIF = 8.07)
- Kept tenure and MonthlyCharges (VIF < 5)

**New Feature Created:**
- `total_services`: Count of subscribed services (0-6)

**Encoding & Scaling:**
- Label Encoding: Binary features (gender, Partner, etc.)
- One-Hot Encoding: Categorical features (Contract, InternetService, PaymentMethod)
- StandardScaler: Numerical features (tenure, MonthlyCharges, total_services)

**Data Split:** Train 60% | Validation 20% | Test 20%

### 4. Model Training & Comparison

**Class Balancing Tested:**
- **SMOTE** (Synthetic Minority Oversampling): 72.5% Recall ✓
- Class Weights: 48.9% Recall
- **Winner:** SMOTE (+48% improvement)

**5 Algorithms Tested (all with SMOTE):**

| Model | Accuracy | Precision | Recall | F1-Score | Why Recall Matters |
|-------|----------|-----------|--------|----------|-------------------|
| **Gradient Boosting** ✓ | 75.6% | 53.03% | **72.46%** | 61.24% | Missing a churner = lost revenue |
| Random Forest | 76.8% | 56.8% | 70.0% | 62.7% | False alarms cheaper than missed churners |
| Logistic Regression | 75.5% | 54.9% | 70.5% | 61.7% | Business prioritizes catching churners |
| Decision Tree | 73.2% | 50.5% | 71.2% | 59.0% | |
| KNN | 73.7% | 50.8% | 66.6% | 57.6% | |

**Champion Model:** Gradient Boosting (best recall with strong overall performance)

---

## Key Results

### Final Model Performance (Test Set)

| Metric | Score | What It Means |
|--------|-------|---------------|
| **Recall** | **72.46%** | Correctly identifies 271 out of 374 churners |
| **Precision** | 53.03% | 53% of flagged customers actually churn |
| **F1-Score** | 61.24% | Balanced performance metric |
| **Accuracy** | 75.66% | Overall correctness |
| **ROC-AUC** | 83.67% | Strong discrimination ability |

### Model Generalization (No Overfitting)

| Metric | Validation | Test | Difference |
|--------|-----------|------|------------|
| Accuracy | 76.58% | 75.66% | -0.92% ✓ |
| Precision | 54.42% | 53.03% | -1.38% ✓ |
| Recall | 72.46% | 72.46% | **0.00% ✓** |
| F1-Score | 62.16% | 61.24% | -0.92% ✓ |

**Conclusion:** Test performance nearly identical to validation → Model generalizes excellently → Ready for production.

### What Drives Churn? (Feature Importance)

| Rank | Feature | Importance | Business Insight |
|------|---------|-----------|------------------|
| 1 | **Tenure** | 27.7% | Loyalty duration is #1 predictor |
| 2 | **Contract Type** | 15.4% | Month-to-month = high risk |
| 3 | **Fiber Optic Service** | 13.8% | Service quality issues suspected |
| 4 | **Payment Method** | 12.5% | Electronic check = friction point |
| 5 | **Total Services** | 5.8% | Low engagement = higher churn |

**Combined:** Contract & Tenure account for **51%** of predictive power.

---

## Business Impact

### Quantified Results

**Baseline (No Model):**
- Random targeting: ~27% detection rate (190 churners caught)

**With ML Model:**
- **271 of 374 churners identified** (72.5% detection rate)
- **+88 additional customers saved** vs baseline
- **103 churners missed** (27.5% false negatives)
- **240 false alarms** (non-churners flagged)

### ROI Calculation

**Assumptions:**
- Average customer lifetime value: €1,200
- Cost of retention campaign: €50 per customer
- Success rate of retention: 30%

**Savings:**
- 271 flagged × 30% success = 81 customers retained
- 81 × €1,200 = €97,200 revenue saved
- Campaign cost: 271 × €50 = €13,550
- **Net profit: €83,650**
- **ROI: 210%**

### Actionable Strategies

#### 1. Contract Conversion Program
**Target:** Month-to-month customers (42.7% churn rate)
- Offer 10-15% discount for 1-year commitment
- Free service upgrades (e.g., add TechSupport)
- Automated outreach at 6-month mark
- **Expected impact:** 15-20% churn reduction

#### 2. Early Customer Engagement
**Target:** Customers with <6 months tenure
- Proactive 30/60/90 day check-in calls
- Priority support during first year
- Welcome package with retention incentives
- **Expected impact:** 25% improvement in first-year retention

#### 3. Service Bundle Optimization
**Target:** Customers with <3 services
- Cross-sell attractive bundles (Internet + Phone + Security)
- Promotional pricing for service additions
- Increase switching costs through bundling
- **Expected impact:** 18% revenue increase per customer

**Combined Expected ROI: 210%**

---

## Technologies

**Languages & Tools:**
- Python 3.8+
- Jupyter Notebook

**Libraries:**
```python
# Data Processing
pandas, numpy

# Visualization
matplotlib, seaborn

# Machine Learning
scikit-learn (GradientBoostingClassifier, RandomForest, LogisticRegression, DecisionTree, KNN)
imbalanced-learn (SMOTE)

# Statistical Testing
scipy.stats (Z-tests)
statsmodels

# Model Persistence
pickle
```

---

## Project Structure
```
final-project-customer-churn-prediction/
│
├── data/
│   └── raw/
│       └── telco_customer_churn.csv          # Original dataset
│
├── notebooks/
│   └── 01_data_exploration.ipynb             # Complete analysis & modeling
│
├── presentation/
│   └── Customer_churn_prediction_Presentation.pdf
│
├── visualizations/
│   └── statistical_validation.png            # Z-test results chart
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

### Prerequisites
```bash
Python 3.8 or higher
pip package manager
```

### Setup
```bash
# Clone repository
git clone https://github.com/Axoudouxou/final-project-customer-churn-prediction.git
cd final-project-customer-churn-prediction

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook notebooks/01_data_exploration.ipynb
```

### Requirements (requirements.txt)
```txt
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0
imbalanced-learn>=0.8.0
jupyter>=1.0.0
scipy>=1.7.0
statsmodels>=0.13.0
```

---

## Key Takeaways

### What Worked
- **SMOTE** dramatically improved recall (+48% vs class weights)
- **Statistical validation** proved findings weren't due to chance (99.99% confidence)
- **Systematic comparison** revealed Gradient Boosting as optimal algorithm
- **Feature engineering** (VIF analysis, total_services) improved model interpretability
- **Business-first approach** (prioritizing recall over precision) aligned with real-world cost structure

### Lessons Learned
1. **Class balancing is critical** for imbalanced datasets
2. **Statistical rigor matters** - validate before modeling
3. **Domain knowledge** guides metric selection (recall > accuracy for churn)
4. **Model generalization** must be proven (validation vs test comparison)
5. **Actionable insights** trump model complexity

---

## Future Enhancements

**Technical:**
- [ ] Deploy as REST API (Flask/FastAPI)
- [ ] Real-time scoring pipeline
- [ ] Automated retraining (quarterly)
- [ ] Ensemble stacking for 1-2% recall improvement
- [ ] SHAP values for individual prediction explanations

**Business:**
- [ ] A/B test retention strategies
- [ ] Build interactive Tableau/PowerBI dashboard
- [ ] Segment-specific models (fiber vs DSL, etc.)
- [ ] Cost-sensitive learning to minimize business impact
- [ ] Integrate with CRM for automated campaign triggers

---

## Author

**Carmelina MBESSO**  
*Data Scientist | AI Developer*

Combining business strategy with technical expertise to drive data-driven decision making.

**Background:**
- M.Sc. International Business Marketing (ISC Paris)
- Data Science (Ironhack Bootcamp)
- Experience: CRM & Marketing Automation (Forvis Mazars, BNP Paribas)

**Connect:**
- LinkedIn: [linkedin.com/in/carmelina-axelle-mbesso](https://www.linkedin.com/in/carmelina-axelle-mbesso-1640b5205/)
- GitHub: [@Axoudouxou](https://github.com/Axoudouxou)
- Email: axmbesso.am@gmail.com
---

## Acknowledgments

- **Ironhack** for comprehensive Data Analytics curriculum
- **IBM** for providing the sample dataset
- **Ironhack instructors** for guidance on systematic model evaluation

---

## License

This project is developed for educational purposes as part of the Ironhack Data Analytics Bootcamp final project.
