from flask import Flask, request, jsonify, render_template
from config import APIKEY
from validators import validate_tick_payload
from business import analyze_tick_payload, get_positions, get_trading_log

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

    try:
        data = request.get_json(force=True)
        print("[DEBUG] tick received data:", data)
    except Exception:
        return jsonify({"result": "failure", "message": "Invalid JSON"}), 400

    is_valid, error_message = validate_tick_payload(data)
    print("[DEBUG] is_valid:", is_valid, "error_message:", error_message)
    if not is_valid:
        return jsonify({"result": "failure", "message": error_message}), 400

    try:
        result = analyze_tick_payload(data)
        print("[DEBUG] /tick response:", result)
        return jsonify(result), 200
    except Exception as e:
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
    app.run(port=5000)
