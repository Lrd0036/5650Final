from flask import Flask, request, jsonify, render_template
from config import API_KEY
from validators import validate_tick_payload
# UPDATED IMPORT: Added get_portfolio_summary from business.py
from business import analyze_tick_payload, get_positions, get_trading_log, get_portfolio_summary 

app = Flask(__name__)

def authenticate():
    """Check if the API key in the request header OR query param is valid."""
    # Check both the header (for tools) AND the URL query args (for browsers)
    api_key = request.headers.get("apikey") or request.args.get("apikey")
    
    if not api_key or api_key != API_KEY:
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

# NEW GEMINI API ENDPOINT: Handles requests from the dashboard's JavaScript
@app.route('/api/summary', methods=['GET'])
def api_summary():
    """Returns the Gemini-generated portfolio summary."""
    # We allow unauthenticated access here because the dashboard is already accessed by the user.
    # If higher security were needed, authenticate() check would be added here.
    try:
        summary_text = get_portfolio_summary()
        return jsonify({"result": "success", "summary": summary_text})
    except Exception as e:
        print(f"[ERROR] Summary generation failed: {str(e)}")
        return jsonify({"result": "failure", "message": f"Summary generation failed: {str(e)}"}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Dashboard view for positions and trading history"""
    try:
        positions = get_positions()
        trading_log = get_trading_log()
        # PASSING API_KEY to template for client-side authentication/requests
        return render_template('dashboard.html', positions=positions, trading_log=trading_log, api_key=API_KEY)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)