import joblib
from azureml.core import Workspace, Model
import numpy as np

class AMLModel:
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
        return self.loaded_model.predict_proba(input_data)

# aml_model = AMLModel(model_name="your_model_name", workspace_config="config.json")

# Load the trained model
model = joblib.load("aml_model.pkl")

def predict_risk_score(features: dict) -> float:
    """Predicts the risk score using the AML model."""
    feature_vector = np.array([
        list(features.values())
    ]).reshape(1, -1)  # Reshape for a single sample

    # Predict proability of fraud
    proba = model.predict_proba(feature_vector)[0][1] #* 100  # Probability of the positive class
    
    return round(proba, 4)
