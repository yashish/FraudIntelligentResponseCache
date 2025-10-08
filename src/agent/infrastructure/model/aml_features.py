# aml_features.py

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