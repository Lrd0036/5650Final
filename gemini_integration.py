import os
import requests
import time
import json 
import random # Used for simple fallback if current_price is missing

# NOTE: This key must be set in your Azure App Service Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") 
# CRITICAL FIX 1: Using the confirmed working model
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# CRITICAL FIX 2: API Key must now be included in the header
HEADERS = {} # Defined inside get_gemini_analysis for fresh key usage

def generate_analysis_prompt(positions, trading_log):
    """Generates a detailed prompt for Gemini based on current data, requesting a JSON time series."""
    
    # Calculate initial total portfolio value (excluding CASH)
    initial_value = sum(
        pos.get('quantity', 0) * pos.get('purchase_price', 0)
        for pos in positions if pos.get('ticker') != 'CASH'
    )
    
    # Safely handle empty list for trading_log
    logs_to_send = trading_log[-5:] if trading_log else []
    trading_log_str = json.dumps(logs_to_send, indent=2) 
    
    # New prompt to generate time-series data for a line graph
    prompt = f"""
    You are an AI financial model tasked with simulating future growth based on current portfolio value.

    **Initial Portfolio Value (Excluding CASH):** ${initial_value:.2f}
    
    **Recent Trading Log (Last 5 Entries):**
{trading_log_str}

    **Instructions:**
    1.  Simulate a total portfolio value projection over the next 10 "days" (time points).
    2.  Start the simulation at Day 0 with the value: ${initial_value:.2f}.
    3.  Generate realistic growth/decline that averages out to a 10% gain over the 10 days, reflecting moderate volatility observed in the trading log.
    4.  Output ONLY a single, valid, strict JSON array following this schema. Do not include any text, headers, markdown fences (```), or explanations outside of the JSON array:
    
    [
        {{"date": "Day 0", "value": {initial_value:.2f}}},
        {{"date": "Day 1", "value": 1250.50}},
        // ... up to Day 10
    ]
    """
    return prompt

def get_gemini_analysis(positions, trading_log):
    """Calls the Gemini API to get structured growth data."""
    if not GEMINI_API_KEY:
        return "ERROR: GEMINI_API_KEY is not configured on the server."
        
    # CRITICAL FIX: Headers must be created fresh here to include the API Key
    HEADERS = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY  # Key placed correctly in the header
    }

    prompt = generate_analysis_prompt(positions, trading_log)
    
    # Payload structure for the Gemini API call
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt 
            }]
        }],
        # System Instruction focuses on generating only JSON
        "systemInstruction": {"parts": [{"text": "You are a financial model that ONLY outputs raw, structured JSON data."}]},
        "generationConfig": {
            "temperature": 0.1, # Low temperature for reliable JSON output
            "maxOutputTokens": 500
        }
    }
    
    for attempt in range(3):
        try:
            # FIX: Sending the request to the base API_URL
            response = requests.post(
                API_URL, 
                headers=HEADERS, 
                json=payload,
                timeout=20
            )
            
            response.raise_for_status() 
            
            result = response.json()
            
            if not result.get('candidates') or not result['candidates'][0].get('content'):
                return f"ERROR: Gemini returned empty content. Response: {result}"

            text = result['candidates'][0]['content']['parts'][0]['text']
            
            # --- Attempt to Parse the Response as JSON ---
            try:
                # Clean up markdown fences often added by the LLM
                if text.strip().startswith('```'):
                    text = text.strip().split('\n', 1)[1] # Remove first line (```json)
                    text = text.rsplit('\n', 1)[0] # Remove last line (```)
                
                parsed_json = json.loads(text)
                return parsed_json # Return the structured data (list of objects)
            except json.JSONDecodeError:
                # If parsing fails, return the error
                return f"ERROR: Gemini returned text that could not be parsed as JSON. Raw output: {text[:200]}..."

        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                error_response_text = response.text
                print(f"[ERROR] 400 Bad Request Payload: {payload}")
                print(f"[ERROR] 400 Bad Request Gemini Detail: {error_response_text}")
                return f"ERROR: 400 Bad Request. Check logs for details. Detail: {error_response_text[:200]}..."
            return f"ERROR: Gemini API HTTP failed after multiple retries. Details: {str(e)}"
                
        except Exception as e:
            return f"ERROR: Could not get a response from the Gemini API. Details: {str(e)}"
            
    return "ERROR: Could not get a response from the Gemini API."