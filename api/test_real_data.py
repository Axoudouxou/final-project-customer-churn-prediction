import requests
import json
import pandas as pd

BASE_URL = "http://127.0.0.1:5001"

# Load real customer data
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Prendre le client 9237-HQITU
churned_customer = df[df['customerID'] == '9237-HQITU'].iloc[0].to_dict()

print("="*80)
print("Testing with HIGH RISK CHURNED customer:")
print("="*80)
print(f"Customer ID: {churned_customer['customerID']}")
print(f"Tenure: {churned_customer['tenure']}")
print(f"Contract: {churned_customer['Contract']}")
print(f"Monthly Charges: {churned_customer['MonthlyCharges']}")
print(f"Actual Churn: {churned_customer['Churn']}")
print()

response = requests.post(f"{BASE_URL}/predict", json=churned_customer)

print("Prediction:")
result = response.json()
print(json.dumps(result, indent=2))

print("\n" + "="*80)
print("ANALYSIS:")
print("="*80)
print(f"Actual: Churned (Yes)")
print(f"Predicted: {'Churn' if result['prediction']['will_churn'] else 'No Churn'}")
print(f"Probability: {result['prediction']['churn_probability']*100:.2f}%")
print(f"Risk Level: {result['risk_assessment']['risk_level']}")

if result['prediction']['will_churn']:
    print("MODEL CORRECT!")
else:
    print("MODEL WRONG - Should predict churn!")