from flask import Flask, request, jsonify, render_template
from config import API_KEY
from validators import validate_tick_payload
# UPDATED IMPORT: Changed to the new local analysis function
from business import analyze_tick_payload, get_positions, get_trading_log, get_chart_growth_data 

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

# CHART DATA API ENDPOINT (Uses local simulation)
@app.route('/api/chart_data', methods=['GET'])
def api_chart_data():
    """Returns the locally calculated time-series growth data."""
    try:
        # Calls the function that uses local_analysis.py
        chart_data = get_chart_growth_data()
        return jsonify({"result": "success", "data": chart_data})
    except Exception as e:
        print(f"[ERROR] Chart data generation failed: {str(e)}")
        return jsonify({"result": "failure", "message": f"Chart data generation failed: {str(e)}"}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Dashboard view for positions and trading history"""
    try:
        positions = get_positions()
        trading_log = get_trading_log()
        # API_KEY is now passed only for client-side authentication for the dashboard features
        return render_template('dashboard.html', positions=positions, trading_log=trading_log, api_key=API_KEY)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)