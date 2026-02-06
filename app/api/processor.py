import asyncio
from app.services.engine import calculate_risk_score
from app.utils.graph_monitor import GraphMonitor
from app.services.llm_analyst import get_ai_justification
from app.services.supabase_client import save_transaction, create_high_confidence_alert


# Initialize our Graph Monitor
monitor = GraphMonitor()

async def process_transaction(tx_data):
    # 1. ML Scoring (The 2,000 alerts level)
    risk_score = calculate_risk_score(tx_data)
    
    # 2. Graph Analysis (Looking for links)
    is_laundering, cycle_path = monitor.add_transaction(
        tx_data['sender_id'], 
        tx_data['receiver_id'], 
        tx_data['amount']
    )

    # 3. Save raw transaction to Supabase (The 'Big Bucket')
    tx_uuid = save_transaction(tx_data, risk_score)

    # 4. The Noise Filter (The '50 alerts' level)
    # We only trigger the LLM and the Alert table if risk is high OR laundering found
    if risk_score > 0.88 or is_laundering:
        # Get the AI to explain WHY
        ai_reason = await get_ai_justification(tx_data, risk_score, is_laundering)
        
        # Push to the 'Alerts' table (Frontend listens to this!)
        create_high_confidence_alert(tx_uuid, ai_reason, is_laundering)
        
        return {"status": "ALERT", "score": risk_score}
    
    return {"status": "CLEARED", "score": risk_score}