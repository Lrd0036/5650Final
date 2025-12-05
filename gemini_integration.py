import os
import requests
import time
import json # <-- CRITICAL: Ensure this is here

# NOTE: This key must be set in your Azure App Service Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") 
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
HEADERS = {'Content-Type': 'application/json'}

def generate_analysis_prompt(positions, trading_log):
    """Generates a detailed prompt for Gemini based on current data."""
    
    positions_str = json.dumps(positions, indent=2)
    # Safely handle empty list for trading_log
    logs_to_send = trading_log[-5:] if trading_log else []
    trading_log_str = json.dumps(logs_to_send, indent=2) 

    prompt = f"""
    You are a world-class financial risk analyst. Analyze the following portfolio data and provide a concise, professional summary for an executive audience.

    **Current Portfolio Positions:**
{positions_str}

    **Recent Trading Log (Last 5 Entries):**
{trading_log_str}

    **Task:**
    1.  Provide a single paragraph **Executive Summary** (100 words max) focusing on overall performance and strategy evident in the recent trades.
    2.  Provide a single paragraph **Risk Assessment** (100 words max) on current diversification (or lack thereof) and potential market exposure.

    Format your response cleanly using only two paragraphs, separated by a newline. Do not use markdown headers (like **, #) in the response text, just plain text.
    """
    return prompt

def get_gemini_analysis(positions, trading_log):
    """Calls the Gemini API to get a portfolio summary and risk assessment."""
    if not GEMINI_API_KEY:
        return "ERROR: GEMINI_API_KEY is not configured on the server."

    prompt = generate_analysis_prompt(positions, trading_log)
    
    # Payload structure for the Gemini API call
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "You are a world-class financial risk analyst who provides professional, concise summaries."}]},
        "config": {
            "temperature": 0.5,
            "maxOutputTokens": 400
        }
    }
    
    # Simple retry mechanism with exponential backoff
    for attempt in range(3):
        try:
            # We explicitly include the key in the URL as confirmed by your error message
            response = requests.post(
                f"{API_URL}?key={GEMINI_API_KEY}", 
                headers=HEADERS, 
                json=payload,
                timeout=20
            )
            response.raise_for_status() # This will raise the 400 error if it occurs
            
            result = response.json()
            
            # Extract the text
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text
            
        except requests.exceptions.RequestException as e:
            # Check if the response content itself might explain the 400 error
            if response.status_code == 400:
                print(f"[ERROR] 400 Bad Request Response: {response.text}")
                return f"ERROR: 400 Bad Request. Possible Invalid Prompt/Data Structure. Response: {response.text[:100]}"
            
            print(f"[ERROR] Gemini API request failed (Attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)  # Exponential backoff (1s, 2s)
            else:
                return f"ERROR: Gemini API failed after multiple retries. Details: {str(e)}"
        except (KeyError, IndexError) as e:
            print(f"[ERROR] Invalid response structure from Gemini: {result}")
            return f"ERROR: Invalid response structure from Gemini. Details: {e}"
            
    return "ERROR: Could not get a response from the Gemini API."