# fraud_features.py
''' Defines the feature schema and encoders for fraud detection.
    This is used both during model training and inference to ensure
    consistent feature processing.
    fraud_features = {
        "transaction_amount": float,          # e.g., 1250.75
        "transaction_type": str,              # e.g., "wire_transfer", "ACH", "crypto"
        "transaction_hour": int,              # e.g., 2 (for off-hour detection)
        "origin_country": str,                # e.g., "US", "NG", "RU"
        "destination_country": str,           # e.g., "US", "AE", "CN"
        "customer_age": int,                  # e.g., 42
        "account_tenure_days": int,           # e.g., 365
        "kyc_verified": bool,                 # True/False
        "prior_fraud_flag": bool,             # True/False
        "device_type": str,                   # e.g., "mobile", "desktop"
        "ip_risk_score": float,               # e.g., 0.92 (from IP reputation service)
        "velocity_score": float               # e.g., 0.85 (based on transaction frequency)     
    }
'''
FEATURE_SCHEMA = [
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

# Optional: categorical mappings
ENCODERS = {
    "transaction_type": {
        "wire_transfer": 0,
        "ACH": 1,
        "crypto": 2,
        "card": 3
    },
    "device_type": {
        "mobile": 0,
        "desktop": 1,
        "tablet": 2,
        "POS": 3,
        "other": 4
    },
    "country": {
        "US": 0,
        "UK": 1,
        "RU": 2,
        "CN": 3,
        "AE": 4
    }
}