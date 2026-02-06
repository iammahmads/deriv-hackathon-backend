import joblib
import pandas as pd
from app.utils.get_fraud_model import get_fraud_model

# Load your pre-trained model (trained on PaySim)
# For the hackathon, you can mock this or train it in 10 mins

def calculate_risk_score(tx: Transaction):
    # 1. Hard Rules (High Priority)
    if tx.amount > 10000 and tx.type == "TRANSFER":
        rule_score = 0.8
    else:
        rule_score = 0.2

    # 2. ML Prediction
    # Convert tx to dataframe format the model expects
    features = pd.DataFrame([tx.dict()])
    model = get_fraud_model()
    ml_prob = model.predict_proba(features)[0][1] 

    # 3. Weighted Final Score
    final_score = (rule_score * 0.4) + (ml_prob * 0.6)
    return final_score