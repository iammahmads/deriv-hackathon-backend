import os
from openai import OpenAI

async def call_llm(tx_data, risk_score, is_laundering, x_openai_key):
    # We add more context like the Graph findings to the prompt
    laundering_context = "CRITICAL: Graph analysis detected a circular money-moving pattern (Money Mule)." if is_laundering else "No circular patterns detected."

    prompt = f"""
    SYSTEM: You are a Senior AML (Anti-Money Laundering) Forensic Auditor. 
    Analyze the following transaction alert and provide a high-confidence verdict.

    DATA:
    - Amount: ${tx_data['amount']}
    - Type: {tx_data['type']}
    - Sender: {tx_data['sender_id']}
    - Receiver: {tx_data['receiver_id']}
    - ML Risk Probability: {risk_score:.2f}
    - Graph Analysis: {laundering_context}

    TASK:
    Provide a 2-sentence highly confident technical justification. 
    Sentence 1: State exactly why this was flagged (e.g., 'Structuring detected via sub-$10k hops' or 'Rapid account depletion').
    Sentence 2: Explain the specific risk to the bank (e.g., 'High probability of synthetic identity layering').
    
    TONE: Confident, Professional, objective, and urgent. No fluff.
    """

    client = OpenAI(api_key=x_openai_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Or gpt-3.5-turbo for speed/cost during the hack
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3 # Low temperature for consistent, professional output
    )

    return response.choices[0].message.content