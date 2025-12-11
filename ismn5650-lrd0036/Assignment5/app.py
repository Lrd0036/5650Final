from flask import Flask, request, jsonify
from config import APIKEY
from validators import validate_tick_payload
from business import analyze_tick_payload

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

@app.route('/tick', methods=['POST'])
def tick():
    """Endpoint to receive and process trading tick data."""
    if not authenticate():
        return jsonify({"result": "failure", "message": "Unauthorized"}), 401
    
    # Parse JSON payload
    try:
        data = request.get_json(force=True)
        print("[DEBUG] tick received data:", data)  # Debug received payload
    except Exception:
        return jsonify({"result": "failure", "message": "Invalid JSON"}), 400
    
    # Validate payload
    is_valid, error_message = validate_tick_payload(data)
    print("[DEBUG] is_valid:", is_valid, "error_message:", error_message)  # Debug validation
    if not is_valid:
        return jsonify({"result": "failure", "message": error_message}), 400
    
    # Process in business layer
    try:
        result = analyze_tick_payload(data)
        print("[DEBUG] /tick response:", result)  # Debug response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"result": "failure", "message": f"Processing error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
