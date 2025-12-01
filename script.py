
# Let me create all the necessary files for Assignment 7

# First, let's generate the config.py with environment variable support
config_content = '''import os
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("APIKEY", "lrd0036")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
MAKE_TRADE_API_KEY = os.getenv("MAKE_TRADE_API_KEY")
MAKE_TRADE_URL = "https://mothership-crg7hzedd6ckfegv.eastus-01.azurewebsites.net/make_trade"
'''

print("config.py content:")
print(config_content)
print("\n" + "="*80 + "\n")

# Create ai_integration.py for ChatGPT integration
ai_integration_content = '''import json
import requests
from openai import OpenAI
from config import CHATGPT_API_KEY

def get_chatgpt_analysis(payload):
    """
    Sends the tick payload to ChatGPT for analysis.
    
    Returns a list of trade decisions in format:
    [
        {"action": "BUY|SELL|STAY", "ticker": "SYMBOL", "quantity": X},
        ...
    ]
    """
    if not CHATGPT_API_KEY:
        raise ValueError("CHATGPT_API_KEY not configured in .env")
    
    client = OpenAI(api_key=CHATGPT_API_KEY)
    
    # Format the market data for ChatGPT
    positions = payload.get("Positions", [])
    market_summary = payload.get("Market_Summary", payload.get("MarketSummary", []))
    market_history = payload.get("market_history", [])
    
    prompt = f"""
You are a trading decision AI. Analyze the current portfolio and market conditions, 
then provide specific BUY/SELL/STAY recommendations for each position.

CURRENT POSITIONS:
{json.dumps(positions, indent=2)}

CURRENT MARKET PRICES:
{json.dumps(market_summary, indent=2)}

MARKET HISTORY (last 2 days):
{json.dumps(market_history, indent=2)}

Based on this data, provide trading recommendations ONLY in the following JSON format:
{{
    "recommendations": [
        {{"action": "BUY", "ticker": "SYMBOL", "quantity": X}},
        {{"action": "SELL", "ticker": "SYMBOL", "quantity": X}},
        {{"action": "STAY", "ticker": "SYMBOL", "quantity": 0}}
    ],
    "reasoning": "Brief explanation of the strategy"
}}

Focus on momentum and price trends. For each position, decide if we should hold, add to, or reduce.
"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a professional trading advisor. Respond ONLY with valid JSON in the specified format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    response_text = response.choices[0].message.content.strip()
    
    # Extract JSON from response
    try:
        # Try to parse directly
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from the response if it's wrapped in text
        import re
        json_match = re.search(r'\\{[^{}]*"recommendations"[^{}]*\\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            raise ValueError(f"Could not parse ChatGPT response: {response_text}")
    
    return result.get("recommendations", [])


def parse_openai_tool_call(response_message):
    """
    Parse tool calls from OpenAI response if using function calling.
    This is an alternative approach using tool definitions.
    """
    if not hasattr(response_message, 'tool_calls') or not response_message.tool_calls:
        return None
    
    for tool_call in response_message.tool_calls:
        if tool_call.function.name == "make_trades":
            return json.loads(tool_call.function.arguments)
    
    return None
'''

print("ai_integration.py content:")
print(ai_integration_content)
print("\n" + "="*80 + "\n")

# Create updated app.py
app_py_content = '''from flask import Flask, request, jsonify, render_template
from config import APIKEY
from validators import validate_tick_payload
from business import analyze_tick_payload, get_positions, get_trading_log
import uuid

app = Flask(__name__)

def authenticate():
    """Check if the API key in the request header is valid."""
    api_key = request.headers.get("apikey")
    if not api_key or api_key != APIKEY:
        return False
    return True

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Health check endpoint."""
    if not authenticate():
        return jsonify({"result": "failure", "message": "Unauthorized"}), 401
    
    try:
        return jsonify({"result": "success", "message": "Ready to Trade"}), 200
    except Exception as e:
        return jsonify({"result": "failure", "message": str(e)}), 500

@app.route('/tick/<string:tick_id>', methods=['POST'])
def tick(tick_id):
    """Endpoint to receive and process trading tick data with a unique ID."""
    if not authenticate():
        return jsonify({"result": "failure", "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json(force=True)
        print(f"[DEBUG] tick received data for ID {tick_id}:", data)
    except Exception:
        return jsonify({"result": "failure", "message": "Invalid JSON"}), 400
    
    is_valid, error_message = validate_tick_payload(data)
    print(f"[DEBUG] is_valid: {is_valid}, error_message: {error_message}")
    
    if not is_valid:
        return jsonify({"result": "failure", "message": error_message}), 400
    
    try:
        result = analyze_tick_payload(data, tick_id)
        print(f"[DEBUG] /tick response:", result)
        return jsonify(result), 200
    except Exception as e:
        print(f"[ERROR] Processing error: {str(e)}")
        return jsonify({"result": "failure", "message": f"Processing error: {str(e)}"}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Dashboard view for positions and trading history"""
    try:
        positions = get_positions()
        trading_log = get_trading_log()
        return render_template('dashboard.html', positions=positions, trading_log=trading_log)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

print("app.py content:")
print(app_py_content)
print("\n" + "="*80 + "\n")

print("Files created successfully. Now generating business.py and other files...")
