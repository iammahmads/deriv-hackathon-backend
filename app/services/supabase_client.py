import os
from supabase import create_client, Client
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def save_transaction(tx_data, score):
    # Insert raw transaction
    response = supabase.table("transactions").insert({
        "tx_id": tx_data['tx_id'],
        "sender_id": tx_data['sender_id'],
        "receiver_id": tx_data['receiver_id'],
        "amount": tx_data['amount'],
        "tx_type": tx_data['type'],
        "risk_score": score,
        "is_flagged": score > 0.85
    }).execute()
    return response.data[0]['id']

def create_high_confidence_alert(tx_uuid, ai_reason, graph_hit, severity="MEDIUM"):
    # Now severity is passed dynamically based on the threat score
    response = supabase.table("alerts").insert({
        "transaction_ref": tx_uuid,
        "severity": severity,
        "ai_summary": ai_reason,
        "graph_detected_laundering": graph_hit
    }).execute()
    
    return response.data[0]['id']

def get_transaction_neighborhood(sender_id: str, receiver_id: str, limit: int = 100):
    """
    Fetches all transactions involving the sender OR the receiver.
    This creates a 'local subgraph' to detect multi-hop laundering.
    """
    try:
        # Use an 'OR' filter to find any transaction where either party was involved
        # This helps detect if Sender -> Middleman -> Receiver
        response = supabase.table("transactions") \
            .select("*") \
            .or_(f"sender_id.eq.{sender_id},receiver_id.eq.{sender_id},sender_id.eq.{receiver_id},receiver_id.eq.{receiver_id}") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return response.data
    except Exception as e:
        print(f"Error fetching neighborhood: {e}")
        return []

def get_transaction_by_id(tx_id: str):
    """Fetches a single transaction by its business ID (tx_id)"""
    response = supabase.table("transactions") \
        .select("*") \
        .eq("tx_id", tx_id) \
        .maybe_single() \
        .execute()
    return response.data


def check_velocity(sender_id: str, threshold: int = 5):
    """
    Checks if a sender has exceeded the transaction limit in the last hour.
    """
    # Calculate time 1 hour ago in ISO format
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    
    try:
        response = supabase.table("transactions") \
            .select("id", count="exact") \
            .eq("sender_id", sender_id) \
            .gte("created_at", one_hour_ago) \
            .execute()
        
        tx_count = response.count if response.count is not None else 0
        
        return tx_count >= threshold, tx_count
    except Exception as e:
        print(f"Velocity Check Error: {e}")
        return False, 0