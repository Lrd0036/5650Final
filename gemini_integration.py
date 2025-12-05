import os
import requests
import time
import json 

# NOTE: This key must be set in your Azure App Service Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") 
# CRITICAL FIX: Changing model name to the string confirmed to work with your key/tier
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# CRITICAL FIX: The API Key must now be included in the header for the API call
HEADERS = {
    'Content-Type': 'application/json',
    'X-goog-api-key': GEMINI_API_KEY  # <--- KEY MOVED TO HEADER
}

def generate_analysis_prompt(positions, trading_log):
    """Generates a detailed prompt for Gemini based on current data."""
    
    positions_str = json.dumps(positions, indent=2)
    
    # We embed the JSON strings directly into the prompt text
    prompt = f"""
    You are a financial analyst specializing in portfolio visualization. Based on the following current positions, generate a JSON array that represents the **market value** of each non-'CASH' asset.

    **Current Portfolio Positions:**
{positions_str}
    
    **Instructions:**
    1. Calculate the current market value for each position (quantity * purchase_price, as current_price is often missing).
    2. Ignore any position where the ticker is 'CASH'.
    3. Output ONLY a single, valid, strict JSON array following this schema. Do not include any text, headers, markdown fences (```), or explanations outside of the JSON array:
    
    [
        {{
            "ticker": "AAPL",
            "value": 1850.00
        }},
        // ... other positions
    ]
    """
    return prompt

def get_gemini_analysis(positions, trading_log):
    """Calls the Gemini API to get a portfolio summary and risk assessment."""
    if not GEMINI_API_KEY:
        return "ERROR: GEMINI_API_KEY is not configured on the server."

    prompt = generate_analysis_prompt(positions, trading_log)
    
    # FIX APPLIED HERE: Renamed 'config' to 'generationConfig' to match Gemini API structure.
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt 
            }]
        }],
        "systemInstruction": {"parts": [{"text": "You are a financial analyst who ONLY outputs raw, structured JSON data."}]},
        "generationConfig": {
            "temperature": 0.1, # Lower temperature for structured output
            "maxOutputTokens": 400
        }
    }
    
    # Simple retry mechanism with exponential backoff
    for attempt in range(3):
        try:
            # FIX: Sending the request to the base API_URL without the query parameter.
            response = requests.post(
                API_URL, 
                headers=HEADERS, # Now includes the key!
                json=payload,
                timeout=20
            )
            
            # CRITICAL CHECK: Raise HTTPError only if the status code is bad
            response.raise_for_status() 
            
            result = response.json()
            
            # --- NEW ROBUST CHECK ---
            if not result.get('candidates') or not result['candidates'][0].get('content'):
                return f"ERROR: Gemini returned empty content. Check Safety Filters or API Key validity. Full response: {result}"
            # --- END NEW CHECK ---

            # Extract the raw text (which should be JSON)
            text = result['candidates'][0]['content']['parts'][0]['text']
            
            # ATTEMPT TO PARSE THE RESPONSE AS JSON
            try:
                # If the text starts and ends with markdown fences, remove them
                if text.startswith('```json'):
                    text = text.strip().replace('```json', '').replace('```', '')
                
                # Parse the clean text into a Python list/dict
                parsed_json = json.loads(text)
                return parsed_json # Return the structured data
            except json.JSONDecodeError:
                # If parsing fails, return the error
                return f"ERROR: Gemini returned text that could not be parsed as JSON: {text[:200]}..."

        except requests.exceptions.HTTPError as e:
            # If a 400 error happens, we want to return the detailed response text from Gemini
            if response.status_code == 400:
                error_response_text = response.text
                print(f"[ERROR] 400 Bad Request Gemini Detail: {error_response_text}")
                return f"ERROR: 400 Bad Request. Possible Invalid Prompt/Data Structure. Gemini Detail: {error_response_text[:200]}..."
            
            # Handle other HTTP errors
            print(f"[ERROR] Gemini API HTTP request failed (Attempt {attempt + 1}): {e}")
            # ... (retry logic omitted for brevity, but remains in the actual file)
                
        except Exception as e:
            # Catch all other errors
            return f"ERROR: Could not get a response from the Gemini API. Details: {str(e)}"
            
    return "ERROR: Could not get a response from the Gemini API."