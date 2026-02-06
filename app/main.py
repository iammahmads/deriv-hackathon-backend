from fastapi import FastAPI, Header
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import os
import pandas as pd
from app.utils.graph_monitor import GraphMonitor
from app.services.llm_analyst import call_llm
from app.services.supabase_client import save_transaction, create_high_confidence_alert, get_transaction_neighborhood, check_velocity
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.utils.get_fraud_model import get_fraud_model

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(["http://localhost:3000", os.getenv("FRONTEND_URL")])),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionPayload(BaseModel):
    tx_id: str = Field(..., min_length=1)
    sender_id: str = Field(..., min_length=1)
    receiver_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    tx_type: str = Field(..., alias="type") # Maps "type" from JSON to tx_type
    features: List[float] = Field(..., min_items=7, max_items=7)

class Config:
    populate_by_name = True


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/analyze")
async def analyze_tx(
    data: TransactionPayload,
    x_openai_key: Optional[str] = Header(None)
):
    try:
        if not x_openai_key or not x_openai_key.startswith("sk-"):
            return {
                "status": "ERROR", 
                "message": "Security Shield: Valid OpenAI API Key required."
            }

        # 1. Behavioral Check (Velocity)
        # Check if this sender is spamming transactions (Potential Smurfing)
        is_high_velocity, v_count = check_velocity(data.sender_id, threshold=5)

        # 2. ML Scoring (Statistical Risk)
        features_df = pd.DataFrame([data.features]) 
        model = get_fraud_model()
        risk_prob = float(model.predict_proba(features_df)[0][1])

        # 3. Graph Analysis (Structural Risk)
        history = get_transaction_neighborhood(data.sender_id, data.receiver_id)
        monitor = GraphMonitor()


        # Build local subgraph context
        for tx in history:
            monitor.add_transaction(tx['sender_id'], tx['receiver_id'], tx['amount'])

        is_laundering, path = monitor.add_transaction(
            data.sender_id, 
            data.receiver_id, 
            data.amount
        )

       # 4. Hybrid Risk Decision Engine
        status = "Clear"
        severity = "LOW"
        ai_reason = "Filtered by Sentinel AI (Low Confidence)"

        if is_high_velocity:
            risk_prob = max(risk_prob, 0.65)
        
        # 5. Persistence
        data_dict = data.model_dump(by_alias=True)
        tx_id = save_transaction(data_dict, risk_prob)

        # 6. Trigger Forensic AI & Alerting
        if risk_prob > 0.70 or is_laundering or is_high_velocity:
            # Call LLM for forensic explanation
            try:
                ai_reason = await call_llm(data_dict, risk_prob, is_laundering, x_openai_key) 
            except Exception:
                ai_reason = "Automated Alert: High-risk indicators detected by Sentinel Engines."

            try:
                # Determine Severity Levels
                if is_laundering and risk_prob > 0.8:
                    severity, status = "CRITICAL", "High Confidence Laundering"
                elif is_laundering or risk_prob > 0.85:
                    severity, status = "HIGH", "Suspicious Pattern Detected"
                elif is_high_velocity or risk_prob > 0.6:
                    severity, status = "MEDIUM", "Behavioral Anomaly"
                
                alert_id = create_high_confidence_alert(tx_id, ai_reason, is_laundering, severity)
                print("Alert created with ID:", alert_id)
            except Exception as e:
                print("Failed to create alert:", e)

        

        return {
            "status": "SUCCESS",
            "risk_score": round(risk_prob * 100, 2),
            "is_laundering": is_laundering,
            "velocity_flag": is_high_velocity,
            "verdict": status,
            "reasoning": ai_reason,
            "severity": severity,
            "internal_id": tx_id
        }
    except Exception as e:
        print(f"Backend Error: {e}")
        return {"status": "ERROR", "message": str(e)}