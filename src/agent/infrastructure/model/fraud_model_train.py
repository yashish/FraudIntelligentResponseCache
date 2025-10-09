# fraud_model_train.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load your AML/KYC dataset
df = pd.read_csv("fraud_aml_kyc_data.csv")

# Feature columns (match your schema)
features = [
    "transaction_amount", 
    "transaction_type_encoded", 
    "transaction_hour",
    "origin_country_encoded",
    "destination_country_encoded", 
    "customer_age", 
    "account_tenure_days",
    "kyc_verified", 
    "prior_fraud_flag", 
    "device_type_encoded",
    "ip_risk_score", 
    "velocity_score"
]

x = df[features]
y = df["is_fraud"]  # binary label: 0 = safe, 1 = fraud

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Save model
joblib.dump(model, "fraud_model.pkl")