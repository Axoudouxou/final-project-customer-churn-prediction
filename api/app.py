from flask import Flask, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)

# Charger le modèle ET le scaler
try:
    with open('churn_model_final_gb_c3.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✓ Model and scaler loaded successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    model = None
    scaler = None

EXPECTED_COLUMNS = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'PaperlessBilling', 'MonthlyCharges', 'total_services',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

def preprocess_customer(data):
    df = pd.DataFrame([data])
    customer_id = df['customerID'].values[0] if 'customerID' in df.columns else 'Unknown'
    
    # Calculer total_services
    service_columns = ['PhoneService', 'InternetService', 'OnlineSecurity',
                      'OnlineBackup', 'DeviceProtection', 'TechSupport',
                      'StreamingTV', 'StreamingMovies']
    df['total_services'] = df[service_columns].apply(lambda x: (x == 'Yes').sum(), axis=1)
    
    # Drop colonnes inutiles
    df = df.drop(columns=['customerID', 'TotalCharges', 'Churn'], errors='ignore')
    
    # Encoder les features binaires
    binary_map = {'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0}
    binary_features = ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_features:
        if col in df.columns:
            df[col] = df[col].map(binary_map)
    
    # One-hot encoding des features catégorielles
    categorical_features = ['MultipleLines', 'InternetService', 'OnlineSecurity',
                           'OnlineBackup', 'DeviceProtection', 'TechSupport',
                           'StreamingTV', 'StreamingMovies', 'Contract', 'PaymentMethod']
    
    for col in categorical_features:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, dummies], axis=1)
            df = df.drop(columns=[col])
    
    # Ajouter les colonnes manquantes
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    
    # Réorganiser dans le bon ordre
    df = df[EXPECTED_COLUMNS]
    
    # SCALER LES DONNÉES (comme dans le notebook)
    cols_to_scale = ['tenure', 'MonthlyCharges', 'total_services']
    if scaler is not None:
        df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    
    return df, customer_id


@app.route('/', methods=['GET'])
def home():
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>Telecom Churn Prediction API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .header p {
                font-size: 1.1em;
                opacity: 0.95;
            }
            .content {
                padding: 40px;
            }
            .section {
                margin-bottom: 40px;
            }
            .section h2 {
                color: #667eea;
                font-size: 1.8em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }
            .info-box {
                background: #f8f9ff;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
            }
            .metric {
                display: inline-block;
                margin: 10px 20px 10px 0;
            }
            .metric-label {
                color: #666;
                font-size: 0.9em;
                display: block;
                margin-bottom: 5px;
            }
            .metric-value {
                color: #667eea;
                font-size: 1.8em;
                font-weight: 700;
            }
            .endpoint {
                background: white;
                border: 2px solid #e0e0e0;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
                transition: all 0.3s;
            }
            .endpoint:hover {
                border-color: #667eea;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
                transform: translateY(-2px);
            }
            .endpoint-method {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 5px;
                font-weight: 700;
                font-size: 0.85em;
                margin-right: 10px;
            }
            .method-get {
                background: #4caf50;
                color: white;
            }
            .method-post {
                background: #2196f3;
                color: white;
            }
            .endpoint-path {
                font-family: 'Courier New', monospace;
                color: #333;
                font-weight: 600;
            }
            .endpoint-desc {
                color: #666;
                margin-top: 10px;
                font-size: 0.95em;
            }
            .risk-levels {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .risk-card {
                padding: 20px;
                border-radius: 10px;
                color: white;
            }
            .risk-high { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            .risk-medium { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
            .risk-low { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
            .risk-card h3 {
                font-size: 1.3em;
                margin-bottom: 10px;
            }
            .risk-card p {
                font-size: 0.9em;
                opacity: 0.95;
            }
            .footer {
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
            .badge {
                display: inline-block;
                padding: 8px 15px;
                background: #4caf50;
                color: white;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
                margin: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 Telecom Churn Prediction API</h1>
                <p>Machine Learning-powered customer retention insights</p>
                <div style="margin-top: 20px;">
                    <span class="badge">Gradient Boosting</span>
                    <span class="badge">SMOTE Balanced</span>
                    <span class="badge">Production Ready</span>
                </div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📊 Model Performance</h2>
                    <div class="info-box">
                        <div class="metric">
                            <span class="metric-label">Recall</span>
                            <span class="metric-value">72.46%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">F1-Score</span>
                            <span class="metric-value">61.24%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Precision</span>
                            <span class="metric-value">53.03%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">ROC-AUC</span>
                            <span class="metric-value">83.67%</span>
                        </div>
                    </div>
                    <p style="color: #666; margin-top: 15px;">
                        Detects <strong>72.5%</strong> of churners (271 out of 374) with targeted retention campaigns.
                    </p>
                </div>

                <div class="section">
                    <h2>🔌 API Endpoints</h2>
                    
                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-path">/health</span>
                        </div>
                        <div class="endpoint-desc">
                            Check API health status and verify model availability
                        </div>
                    </div>

                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-post">POST</span>
                            <span class="endpoint-path">/predict</span>
                        </div>
                        <div class="endpoint-desc">
                            Submit customer data to receive churn prediction, probability score, and risk assessment
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>⚠️ Risk Classification</h2>
                    <div class="risk-levels">
                        <div class="risk-card risk-high">
                            <h3>High Risk (≥70%)</h3>
                            <p>Immediate intervention required. Priority for retention team.</p>
                        </div>
                        <div class="risk-card risk-medium">
                            <h3>Medium Risk (40-70%)</h3>
                            <p>Monitor closely and engage with targeted offers.</p>
                        </div>
                        <div class="risk-card risk-low">
                            <h3>Low Risk (<40%)</h3>
                            <p>Continue standard service and relationship building.</p>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>💡 Business Impact</h2>
                    <div class="info-box">
                        <p style="margin-bottom: 10px;"><strong>Customer Lifetime Value Protection:</strong></p>
                        <ul style="margin-left: 20px; color: #666; line-height: 1.8;">
                            <li>Average CLTV per retained customer: <strong>$3,456</strong></li>
                            <li>Campaign cost per customer: <strong>~$150</strong></li>
                            <li>Estimated ROI: <strong>210%</strong> (if 5% conversion achieved)</li>
                            <li>Annual revenue protection: <strong>$924,358</strong></li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="footer">
                <p><strong>Telecom Churn Prediction API v1.0</strong></p>
                <p>Developed for RNCP Data Analytics Certification | February 2026</p>
            </div>
        </div>
    </body>
    </html>"""


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy' if (model and scaler) else 'unhealthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None or scaler is None:
            return jsonify({'error': 'Model or scaler not loaded'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df, customer_id = preprocess_customer(data)
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0]
        churn_prob = probability[1]
        
        if churn_prob >= 0.7:
            risk_level, action = 'High', 'Immediate intervention required'
        elif churn_prob >= 0.4:
            risk_level, action = 'Medium', 'Monitor and engage with retention offers'
        else:
            risk_level, action = 'Low', 'Continue standard service'
        
        return jsonify({
            'customer_id': customer_id,
            'prediction': {
                'will_churn': bool(prediction),
                'churn_probability': round(float(churn_prob), 4),
                'retention_probability': round(float(probability[0]), 4)
            },
            'risk_assessment': {
                'risk_level': risk_level,
                'recommended_action': action
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("="*60)
    print("Telecom Churn Prediction API")
    print("="*60)
    print("API available at: http://127.0.0.1:5001")
    print("")
    print("Endpoints:")
    print("  GET  /          - API documentation")
    print("  GET  /health    - Health check")
    print("  POST /predict   - Churn prediction")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)