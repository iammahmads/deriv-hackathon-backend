import requests
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = f"{BASE_URL}/v1/analyze"

def generate_features(is_fraud=False):
    if is_fraud:
        # Scenario: Emptying a high-value account (Typical Fraud)
        amount = random.uniform(900000, 2000000)
        oldbalanceOrg = amount + random.uniform(0, 500)
        newbalanceOrig = 0 # Account wiped
        oldbalanceDest = 0
        newbalanceDest = amount
    else:
        # Scenario: Normal small transfer
        amount = random.uniform(10, 500)
        oldbalanceOrg = random.uniform(1000, 5000)
        newbalanceOrig = oldbalanceOrg - amount
        oldbalanceDest = random.uniform(100, 2000)
        newbalanceDest = oldbalanceDest + amount

    # Calculate the 'Hidden' features the model loves
    errorBalanceSender = amount + newbalanceOrig - oldbalanceOrg
    errorBalanceReceiver = oldbalanceDest + amount - newbalanceDest

    return [
        amount, 
        oldbalanceOrg, 
        newbalanceOrig, 
        oldbalanceDest, 
        newbalanceDest, 
        errorBalanceSender, 
        errorBalanceReceiver
    ]

def send_mock_tx():
    is_suspicious = random.random() > 0.3
    features_list = generate_features(is_fraud=is_suspicious)

    print("is_suspicious", is_suspicious)
    
    payload = {
        "tx_id": f"TX-{random.randint(1000, 9999)}",
        "sender_id": "user_a" if not is_suspicious else "mule_1",
        "receiver_id": "user_b" if not is_suspicious else "mule_2",
        "amount": features_list[0], # Use the amount from features for consistency
        "type": "TRANSFER",
        "features": features_list
    }
    
    try:
        headers = {
            "Content-Type": "application/json",
            "X-OpenAI-Key": OPENAI_API_KEY
        }

        res = requests.post(API_URL, json=payload, headers=headers)

        
        # Check if the server actually succeeded
        if res.status_code == 200 and res.json().get("status") == "SUCCESS":
            data = res.json()
            risk_score = data.get("risk_score")
            risk_score_str = f"{risk_score:.4f}" if isinstance(risk_score, (int, float)) else "N/A"
            print(
                f"""
            🧾 Transaction Result
            --------------------
            TX ID: {data.get('internal_id')}
            Verdict: {data.get('verdict')}
            Laundering Detected: {data.get('is_laundering')}
            Risk Score: {risk_score_str}
            Severity: {data.get('severity')}
            Reasoning: {data.get('reasoning')}
            Velocity Flag: {data.get('velocity_flag')}
            """
            )

            # urn {
            # "status": "SUCCESS",
            # "risk_score": round(risk_prob * 100, 2),
            # "is_laundering": is_laundering,
            # "velocity_flag": is_high_velocity,
            # "verdict": status,
            # "reasoning": ai_reason,
            # "severity": severity,
            # "internal_id": tx_uuid

        else:
            print(f"❌ Server Error ({res.status_code}): {res.text[:100]}")
            
    except Exception as e:
        print(f"🚨 Network Error: {e}")


if __name__ == "__main__":
    print("🚀 Transaction Simulator started")
    send_mock_tx()
    # while True:
    #     send_mock_tx()
    #     time.sleep(10)