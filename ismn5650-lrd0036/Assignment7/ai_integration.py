import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Expect CHATGPT_API_KEY or fallback to OPENAI_API_KEY for flexibility
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in CHATGPT_API_KEY or OPENAI_API_KEY environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_chatgpt_analysis(payload):
    """
    Sends trading tick payload to GPT-5 Nano for structured trade recommendations.
    Returns list of trade decisions:
    [ {"action": "BUY|SELL|STAY", "ticker": "SYMBOL", "quantity": X}, ... ]
    """
    positions = payload.get("Positions", payload.get("positions", []))
    market_summary = (
        payload.get("Market_Summary") or
        payload.get("MarketSummary") or
        payload.get("market_summary") or
        payload.get("marketSummary") or []
    )
    market_history = payload.get("market_history", [])

    prompt = f"""
You are a professional trading advisor AI. Analyze the portfolio positions, current market prices, and recent market history.

CURRENT POSITIONS:
{json.dumps(positions, indent=2)}

MARKET SUMMARY:
{json.dumps(market_summary, indent=2)}

MARKET HISTORY (last 2 days):
{json.dumps(market_history, indent=2)}

Provide your trading recommendations ONLY in the following JSON format (no other text):
{{
    "recommendations": [
        {{"action": "BUY", "ticker": "SYMBOL", "quantity": X}},
        {{"action": "SELL", "ticker": "SYMBOL", "quantity": X}},
        {{"action": "STAY", "ticker": "SYMBOL", "quantity": 0}}
    ],
    "reasoning": "Brief reasoning for your choices"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a professional trading advisor. Respond ONLY with valid JSON in the specified format. No additional text."},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
        )
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        raise RuntimeError(f"OpenAI API call failed: {e}")

    response_text = response.choices[0].message.content.strip()
    print(f"[DEBUG] GPT-5-Nano response: {response_text}")

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # Extract JSON if response contains extra text
        json_match = re.search(r'{.*"recommendations".*}', response_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to parse extracted JSON: {e}")
                raise ValueError(f"Could not parse response as valid JSON: {response_text}")
        else:
            print(f"[ERROR] No JSON found in response: {response_text}")
            raise ValueError(f"Could not parse response as valid JSON: {response_text}")

    recommendations = result.get("recommendations", [])
    reasoning = result.get("reasoning", "")

    print(f"[DEBUG] Trading reasoning: {reasoning}")
    print(f"[DEBUG] Recommendations: {recommendations}")

    if not recommendations:
        # If no recommendations, return stay for all positions
        recommendations = [
            {"action": "STAY", "ticker": pos.get("ticker"), "quantity": 0}
            for pos in positions
        ]
        print("[DEBUG] No recommendations from GPT; returning STAY for all positions.")

    return recommendations

if __name__ == "__main__":
    # Test with sample payload
    sample_payload = {
        "Positions": [
            {"ticker": "AAPL", "quantity": 6, "purchase_price": 150},
            {"ticker": "MSFT", "quantity": 3, "purchase_price": 300}
        ],
        "Market_Summary": [
            {"ticker": "AAPL", "current_price": 170},
            {"ticker": "MSFT", "current_price": 325}
        ],
        "market_history": []
    }
    ##trades = get_chatgpt_analysis(sample_payload)
    ##print("Trade Decisions:", trades)
