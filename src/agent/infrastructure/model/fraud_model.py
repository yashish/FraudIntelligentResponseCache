import joblib
#from azureml.core import Workspace, Model
import numpy as np
from fraud_features import FEATURE_SCHEMA, ENCODERS

""" class AMLModel:
    def __init__(self, model_name: str, workspace_config: str):
        self.workspace = Workspace.from_config(path=workspace_config)
        self.model = Model(self.workspace, name=model_name)
        self.model_path = self.model.download(exist_ok=True)
        self.loaded_model = joblib.load(self.model_path)

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        return self.loaded_model.predict(input_data)
    
# Example usage:
# aml_model = AMLModel(model_name="your_model_name", workspace_config="config.json")
    def predict_proba(self, input_data: np.ndarray) -> np.ndarray:
        return self.loaded_model.predict_proba(input_data) """

# aml_model = AMLModel(model_name="your_model_name", workspace_config="config.json")

# Load the trained model
model = joblib.load("fraud_model.pkl")

def encode_input(raw: dict) -> list[float]:
    return [
        raw["transaction_amount"],
        ENCODERS["transaction_type"].get(raw["transaction_type"], -1),
        raw["transaction_hour"]
        ENCODERS["country"].get(raw["origin_country"], -1),
        ENCODERS["country"].get(raw["destination_country"], -1),
        raw["customer_age"],
        raw["account_tenure_days"],
        int(raw["kyc_verified"]),
        int(raw["prior_fraud_flag"]),
        ENCODERS["device_type"].get(raw["device_type"], -1),
        raw["ip_risk_score"],
        raw["velocity_score"]
    ]

def predict_risk_score(features: dict) -> float:
    """Predicts the risk score using the AML model."""
    # Ensure all required features are present
    # missing = [f for f in FEATURE_SCHEMA if f not in features]
    # if missing:
    #     raise ValueError(f"Missing features for prediction: {missing}")

    # Encode and reshape input features
    feature_vector = np.array([
        encode_input(features)
    ]).reshape(1, -1) # Reshape for a single sample

    # Predict proability of fraud
    proba = model.predict_proba(feature_vector)[0][1] #* 100  # Probability of the positive class
    
    return round(proba, 4)
