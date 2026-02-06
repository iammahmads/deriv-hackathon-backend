import joblib
import os

# Initialize as None
_model = None

def get_fraud_model():
    global _model  # Crucial for persistent state
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "../models/fraud_model.pkl")
        try:
            _model = joblib.load(model_path)
            print("✅ Fraud model loaded into memory.")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            raise e
    return _model