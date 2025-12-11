"""
Tester for Strategy AI Agent — Part 1 (API Server)
Validates:
- Auth (header 'apikey')
- /healthcheck behavior
- /tick validation & happy path
"""

import requests
from math import isclose

BASE_URL = "http://127.0.0.1:5000"
API_KEY = "lrd0036"   # e.g., jaf0070
TIMEOUT = 6

def h(ok): return "✅ PASS" if ok else "❌ FAIL"

def j(resp):
    try: return resp.json()
    except Exception: return None

def headers(ok=True):
    return {"apikey": API_KEY if ok else "WRONG_KEY"}

def test_health_auth():
    # Without key -> should be 401
    r1 = requests.get(f"{BASE_URL}/healthcheck", headers=headers(False), timeout=TIMEOUT)
    body1 = j(r1)
    ok1 = (r1.status_code == 401 and isinstance(body1, dict) and body1.get("result") == "failure")

    # With correct key -> should be 200 success
    r2 = requests.get(f"{BASE_URL}/healthcheck", headers=headers(), timeout=TIMEOUT)
    body2 = j(r2)
    ok2 = (r2.status_code == 200 and isinstance(body2, dict) and body2.get("result") == "success")

    print("/healthcheck requires and validates API key:", h(ok1 and ok2))


def test_tick_auth_required():
    r = requests.post(f"{BASE_URL}/tick", json={}, headers=headers(False), timeout=TIMEOUT)
    body = j(r)
    ok = (r.status_code == 401 and isinstance(body, dict) and body.get("result") == "failure")
    print("Auth required on /tick:", h(ok))

def test_tick_validation_errors():
    # Not JSON
    r1 = requests.post(f"{BASE_URL}/tick", data="nope", headers=headers(), timeout=TIMEOUT)
    # Missing keys
    r2 = requests.post(f"{BASE_URL}/tick", json={"Positions": []}, headers=headers(), timeout=TIMEOUT)
    ok = (r1.status_code == 400 or r1.status_code == 401) and (r2.status_code == 400)
    print("/tick validation errors handled:", h(ok))

def make_payload():
    return {
        "Positions": [
            {"ticker": "AAPL", "quantity": 10, "purchase_price": 180.0},
            {"ticker": "MSFT", "quantity": 5, "purchase_price": 410.0}
        ],
        "Market_Summary": [
            {"ticker": "AAPL", "current_price": 182.5},
            {"ticker": "MSFT", "current_price": 405.0}
        ],
        "market_history": [
            {"ticker": "AAPL", "price": 179.8, "day": 1},
            {"ticker": "AAPL", "price": 181.2, "day": 2},
            {"ticker": "MSFT", "price": 409.5, "day": 1},
            {"ticker": "MSFT", "price": 405.0, "day": 2}
        ]
    }

def expected_pnl(payload):
    curr = {r["ticker"]: float(r["current_price"]) for r in payload["Market_Summary"]}
    pnl = 0.0
    for p in payload["Positions"]:
        t = p["ticker"]; q = float(p["quantity"]); cost = float(p["purchase_price"])
        if t in curr:
            pnl += (curr[t] - cost) * q
    return pnl

def test_tick_success():
    payload = make_payload()
    r = requests.post(f"{BASE_URL}/tick", json=payload, headers=headers(), timeout=TIMEOUT)
    body = j(r)
    if r.status_code != 200 or not isinstance(body, dict):
        print("/tick success:", h(False)); return

    # Check structure
    has_fields = body.get("result") == "success" and "summary" in body and "decisions" in body
    if not has_fields:
        print("/tick success (shape):", h(False)); return

    # Check P&L approximately
    got = float(body["summary"].get("unrealized_pnl", 999999))
    exp = expected_pnl(payload)
    ok = isclose(got, exp, rel_tol=1e-9, abs_tol=1e-9)
    print("/tick success (math):", h(ok))

def main():
    print("== Strategy AI Agent — Part 1 Tester ==")
    if API_KEY == "PUT_STUDENT_USERNAME_HERE":
        print("WARNING: Set API_KEY to the student's username.\n")

    # ping server root (optional)
    try:
        requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
    except Exception as e:
        print(f"Could not reach server at {BASE_URL}. Is it running?\nDetails: {e}")
        return

    test_health_auth()
    test_tick_auth_required()
    test_tick_validation_errors()
    test_tick_success()
    print("\nDone.")

if __name__ == "__main__":
    main()
