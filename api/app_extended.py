from flask import Flask, jsonify, request
import pickle
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ============================================
# CONFIGURATION MySQL
# ============================================
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '26052002', 
    'database': 'telco_churn'  
}

def get_db_connection():
    """Create MySQL database connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except Error as e:
        print(f"MySQL Error: {e}")
        return None

# ============================================
# LOAD ML MODEL
# ============================================
try:
    with open('churn_model_final_gb_c3.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("Model and scaler loaded successfully")
except Exception as e:
    print(f" Error: {e}")
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
    
    # One-hot encoding
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
    
    # Réorganiser
    df = df[EXPECTED_COLUMNS]
    
    # SCALER
    cols_to_scale = ['tenure', 'MonthlyCharges', 'total_services']
    if scaler is not None:
        df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    
    return df, customer_id


# ============================================
# EXISTING ENDPOINTS (HOME, HEALTH, PREDICT)
# ============================================

@app.route('/', methods=['GET'])
def home():
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>Telecom Churn Prediction API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 1000px;
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
            .content { padding: 40px; }
            .section { margin-bottom: 40px; }
            .section h2 {
                color: #667eea;
                font-size: 1.8em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
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
            .method-get { background: #4caf50; color: white; }
            .method-post { background: #2196f3; color: white; }
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
            .footer {
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 Telecom Churn Prediction API</h1>
                <p>RESTful API with 2 Resources & 5 Endpoints</p>
                <div style="margin-top: 20px;">
                    <span class="badge">REST Architecture</span>
                    <span class="badge">Pagination</span>
                    <span class="badge">MySQL Integration</span>
                </div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📌 Resource 1: Customers</h2>
                    
                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-path">/api/customers?limit=20&offset=0&churn=Yes</span>
                        </div>
                        <div class="endpoint-desc">
                            Returns paginated list of customers with optional filters
                            <br><strong>Filters:</strong> churn (Yes/No), contract (Month-to-month/One year/Two year), senior_citizen (0/1)
                        </div>
                    </div>

                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-path">/api/customers/{customer_id}</span>
                        </div>
                        <div class="endpoint-desc">
                            Returns complete profile for a single customer (joins 6 MySQL tables)
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>🎯 Resource 2: Predictions</h2>
                    
                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-path">/api/predictions?limit=10&risk_level=High</span>
                        </div>
                        <div class="endpoint-desc">
                            Returns historical predictions with optional risk level filter
                            <br><strong>Filters:</strong> risk_level (High/Medium/Low)
                        </div>
                    </div>

                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-post">POST</span>
                            <span class="endpoint-path">/api/predictions</span>
                        </div>
                        <div class="endpoint-desc">
                            Submit customer data to receive real-time churn prediction
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>⚡ System Endpoints</h2>
                    
                    <div class="endpoint">
                        <div>
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-path">/health</span>
                        </div>
                        <div class="endpoint-desc">
                            API health check and model status verification
                        </div>
                    </div>
                </div>
            </div>

            <div class="footer">
                <p><strong>Telecom Churn Prediction API v2.0</strong></p>
                <p>RNCP Data Analytics Project | February 2026</p>
            </div>
        </div>
    </body>
    </html>"""


@app.route('/health', methods=['GET'])
def health():
    # Test MySQL connection
    db_connection = get_db_connection()
    db_status = 'connected' if db_connection else 'disconnected'
    if db_connection:
        db_connection.close()
    
    return jsonify({
        'status': 'healthy' if (model and scaler and db_connection) else 'partial',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'database_status': db_status
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Original prediction endpoint (renamed to /api/predictions for REST consistency)"""
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


# ============================================
# NEW ENDPOINTS - REST API
# ============================================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """
    GET /api/customers?limit=20&offset=0&churn=Yes&contract=Month-to-month
    
    Returns paginated list of customers with optional filters
    """
    try:
        # Pagination parameters
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        # Validation
        if limit > 100:
            return jsonify({'error': 'Maximum limit is 100'}), 400
        if limit < 1:
            return jsonify({'error': 'Minimum limit is 1'}), 400
        
        # Filter parameters
        churn_filter = request.args.get('churn')  # "Yes" or "No"
        contract_filter = request.args.get('contract')
        senior_filter = request.args.get('senior_citizen')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query dynamically
        query = """
            SELECT 
                d.customer_id,
                d.gender,
                d.senior_citizen,
                d.married as partner,
                d.dependents,
                s.tenure_in_months as tenure,
                s.contract,
                s.monthly_charge,
                s.total_charges,
                st.churn_label as churn,
                st.churn_category,
                st.churn_score,
                st.cltv,
                l.city,
                l.state
            FROM customers_demographics d
            JOIN customers_services s ON d.customer_id = s.customer_id
            JOIN customers_status st ON d.customer_id = st.customer_id
            JOIN customers_location l ON d.customer_id = l.customer_id
            WHERE 1=1
        """
        
        params = []
        
        # Apply filters
        if churn_filter:
            query += " AND st.churn_label = %s"
            params.append(churn_filter)
        if contract_filter:
            query += " AND s.contract = %s"
            params.append(contract_filter)
        if senior_filter:
            query += " AND d.senior_citizen = %s"
            params.append(senior_filter)
        
        # Count total matching records
        count_query = query.replace(
            "SELECT d.customer_id", 
            "SELECT COUNT(*) as total"
        ).replace("FROM customers_demographics d", "FROM customers_demographics d", 1)
        # Remove the columns from SELECT for count
        count_query = f"SELECT COUNT(*) as total FROM customers_demographics d JOIN customers_services s ON d.customer_id = s.customer_id JOIN customers_status st ON d.customer_id = st.customer_id JOIN customers_location l ON d.customer_id = l.customer_id WHERE 1=1"
        if churn_filter:
            count_query += " AND st.churn_label = %s"
        if contract_filter:
            count_query += " AND s.contract = %s"
        if senior_filter:
            count_query += " AND d.senior_citizen = %s"
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Add pagination
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        customers = cursor.fetchall()
        
        # Build response
        response = {
            'metadata': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'page': (offset // limit) + 1,
                'total_pages': (total + limit - 1) // limit
            },
            'data': customers
        }
        
        # Add pagination links
        if offset + limit < total:
            next_params = f"?limit={limit}&offset={offset + limit}"
            if churn_filter:
                next_params += f"&churn={churn_filter}"
            if contract_filter:
                next_params += f"&contract={contract_filter}"
            response['links'] = {
                'next': f"/api/customers{next_params}"
            }
        
        if offset > 0:
            prev_offset = max(0, offset - limit)
            prev_params = f"?limit={limit}&offset={prev_offset}"
            if churn_filter:
                prev_params += f"&churn={churn_filter}"
            if contract_filter:
                prev_params += f"&contract={contract_filter}"
            if 'links' not in response:
                response['links'] = {}
            response['links']['previous'] = f"/api/customers{prev_params}"
        
        cursor.close()
        connection.close()
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """
    GET /api/customers/{customer_id}
    
    Returns complete profile for a single customer
    """
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Query joining all 6 tables
        query = """
            SELECT 
                d.customer_id,
                d.gender,
                d.age,
                d.senior_citizen,
                d.married as partner,
                d.dependents,
                d.number_of_dependents,
                s.quarter,
                s.tenure_in_months as tenure,
                s.phone_service,
                s.internet_service,
                s.internet_type,
                s.contract,
                s.payment_method,
                s.monthly_charge,
                s.total_charges,
                st.satisfaction_score,
                st.churn_label,
                st.churn_value,
                st.churn_score,
                st.cltv,
                st.churn_category,
                st.churn_reason,
                l.country,
                l.state,
                l.city,
                l.zip_code,
                l.latitude,
                l.longitude,
                zc.median_income,
                zc.population_below_poverty,
                zc.unemployed_population,
                zp.population
            FROM customers_demographics d
            JOIN customers_services s ON d.customer_id = s.customer_id
            JOIN customers_status st ON d.customer_id = st.customer_id
            JOIN customers_location l ON d.customer_id = l.customer_id
            LEFT JOIN zip_census_data zc ON l.zip_code = zc.zip_code
            LEFT JOIN zip_population zp ON l.zip_code = zp.zip_code
            WHERE d.customer_id = %s
        """
        
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Structure response with nesting
        response = {
            'customer_id': customer['customer_id'],
            'demographics': {
                'gender': customer['gender'],
                'age': customer['age'],
                'senior_citizen': bool(customer['senior_citizen']),
                'partner': customer['partner'],
                'dependents': customer['dependents'],
                'number_of_dependents': customer['number_of_dependents']
            },
            'services': {
                'quarter': customer['quarter'],
                'tenure_months': customer['tenure'],
                'phone_service': customer['phone_service'],
                'internet_service': customer['internet_service'],
                'internet_type': customer['internet_type'],
                'contract': customer['contract'],
                'payment_method': customer['payment_method']
            },
            'billing': {
                'monthly_charge': float(customer['monthly_charge']) if customer['monthly_charge'] else None,
                'total_charges': float(customer['total_charges']) if customer['total_charges'] else None,
                'cltv': customer['cltv']
            },
            'location': {
                'country': customer['country'],
                'state': customer['state'],
                'city': customer['city'],
                'zip_code': customer['zip_code'],
                'latitude': float(customer['latitude']) if customer['latitude'] else None,
                'longitude': float(customer['longitude']) if customer['longitude'] else None
            },
            'census_data': {
                'median_income': float(customer['median_income']) if customer['median_income'] else None,
                'population': customer['population'],
                'population_below_poverty': customer['population_below_poverty'],
                'unemployed_population': customer['unemployed_population']
            },
            'churn_status': {
                'churned': customer['churn_label'],
                'churn_value': customer['churn_value'],
                'churn_score': customer['churn_score'],
                'churn_category': customer['churn_category'],
                'churn_reason': customer['churn_reason'],
                'satisfaction_score': customer['satisfaction_score']
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """
    GET /api/predictions?limit=10&risk_level=High
    
    Returns historical predictions (simulated from churn_score)
    """
    try:
        limit = int(request.args.get('limit', 10))
        risk_filter = request.args.get('risk_level')  # "High", "Medium", "Low"
        
        if limit > 100:
            return jsonify({'error': 'Maximum limit is 100'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                d.customer_id,
                st.churn_score,
                CASE 
                    WHEN st.churn_score >= 70 THEN 'High'
                    WHEN st.churn_score >= 40 THEN 'Medium'
                    ELSE 'Low'
                END as risk_level,
                st.churn_label as actual_churn,
                s.contract,
                s.monthly_charge,
                st.cltv
            FROM customers_demographics d
            JOIN customers_status st ON d.customer_id = st.customer_id
            JOIN customers_services s ON d.customer_id = s.customer_id
            WHERE st.churn_score IS NOT NULL
        """
        
        params = []
        
        if risk_filter:
            query += """
                HAVING risk_level = %s
            """
            params.append(risk_filter)
        
        query += " ORDER BY st.churn_score DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        predictions = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Format response
        response = {
            'total': len(predictions),
            'limit': limit,
            'data': [
                {
                    'customer_id': p['customer_id'],
                    'churn_probability': p['churn_score'] / 100.0,
                    'risk_level': p['risk_level'],
                    'actual_churn': p['actual_churn'],
                    'contract': p['contract'],
                    'monthly_charge': float(p['monthly_charge']) if p['monthly_charge'] else None,
                    'cltv': p['cltv']
                }
                for p in predictions
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# ALIAS FOR REST CONSISTENCY
# ============================================
@app.route('/api/predictions', methods=['POST'])
def create_prediction():
    """Alias for /predict endpoint to maintain REST consistency"""
    return predict()


# ============================================
# RUN APP
# ============================================
if __name__ == '__main__':
    print("="*70)
    print("🚀 Telecom Churn Prediction API - RESTful Edition")
    print("="*70)
    print("API available at: http://127.0.0.1:5001")
    print("")
    print("📋 Resource 1: Customers")
    print("  GET  /api/customers              - Paginated customer list")
    print("  GET  /api/customers/{id}         - Single customer details")
    print("")
    print("🎯 Resource 2: Predictions")
    print("  GET  /api/predictions            - Historical predictions")
    print("  POST /api/predictions            - Create prediction")
    print("  POST /predict                    - Legacy endpoint (same as above)")
    print("")
    print("⚡ System")
    print("  GET  /                           - API documentation")
    print("  GET  /health                     - Health check")
    print("="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
