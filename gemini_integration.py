import os
import requests
import time
import json 

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

    # We embed the JSON strings directly into the prompt text
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
    
    # FIX APPLIED HERE: Renamed 'config' to 'generationConfig' to match Gemini API structure.
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt 
            }]
        }],
        "systemInstruction": {"parts": [{"text": "You are a world-class financial risk analyst who provides professional, concise summaries."}]},
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 400
        }
    }
    
    # Simple retry mechanism with exponential backoff
    for attempt in range(3):
        try:
            # We explicitly include the key in the URL 
            response = requests.post(
                f"{API_URL}?key={GEMINI_API_KEY}", 
                headers=HEADERS, 
                json=payload,
                timeout=20
            )
            
            # CRITICAL CHECK: Raise HTTPError only if the status code is bad
            response.raise_for_status() 
            
            result = response.json()
            
            # --- NEW ROBUST CHECK ---
            if not result.get('candidates') or not result['candidates'][0].get('content'):
                # This handles safety filters or empty content errors cleanly
                return f"ERROR: Gemini returned empty content. Check Safety Filters or API Key validity. Full response: {result}"
            # --- END NEW CHECK ---

            # Extract the text
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text
            
        except requests.exceptions.HTTPError as e:
            # If a 400 error happens, we want to return the detailed response text from Gemini
            if response.status_code == 400:
                error_response_text = response.text
                print(f"[ERROR] 400 Bad Request Payload: {payload}")
                print(f"[ERROR] 400 Bad Request Gemini Detail: {error_response_text}")
                # This return message is now highly detailed for easier debugging
                return f"ERROR: 400 Bad Request. Possible Invalid Prompt/Data Structure. Gemini Detail: {error_response_text[:200]}..."
            
            # Handle other HTTP errors
            print(f"[ERROR] Gemini API HTTP request failed (Attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return f"ERROR: Gemini API failed after multiple HTTP retries. Details: {str(e)}"
                
        except requests.exceptions.RequestException as e:
             # Handle non-HTTP exceptions (connection, timeout)
            print(f"[ERROR] Gemini API non-HTTP request failed (Attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return f"ERROR: Gemini API failed after multiple retries. Details: {str(e)}"
                
        except (KeyError, IndexError) as e:
            print(f"[ERROR] Invalid response structure from Gemini: {result}")
            return f"ERROR: Invalid response structure from Gemini. Details: {e}"
            
    return "ERROR: Could not get a response from the Gemini API."