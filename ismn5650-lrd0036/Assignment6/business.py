import json
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSITIONS_FILE = os.path.join(CURRENT_DIR, "Assignment6PositionsSample.txt")
TRADING_LOG_FILE = os.path.join(CURRENT_DIR, "Assignment6TradingLogSample.txt")

def analyze_tick_payload(payload):
    positions = payload.get("Positions", payload.get("positions", []))
    # Supports MarketSummary, Market_Summary, or marketSummary
    if "MarketSummary" in payload:
        market_summary = payload.get("MarketSummary")
    elif "Market_Summary" in payload:
        market_summary = payload.get("Market_Summary")
    else:
        market_summary = payload.get("marketSummary", [])

    current_prices = {}
    for item in market_summary:
        ticker = item.get("ticker")
        current_price = item.get("currentprice", item.get("current_price"))
        if ticker and current_price is not None:
            current_prices[ticker] = float(current_price)

    unrealized_pnl = 0.0
    positions_evaluated = 0

    # Update positions for dashboard data: persist to file
    updated_positions = []
    for position in positions:
        ticker = position.get("ticker")
        quantity = float(position.get("quantity", 0))
        purchase_price = position.get("purchaseprice", position.get("purchase_price"))
        if ticker in current_prices and purchase_price is not None:
            current_price = current_prices[ticker]
            pnl = (current_price - float(purchase_price)) * quantity
            unrealized_pnl += pnl
            positions_evaluated += 1
            updated_pos = {
                "ticker": ticker,
                "quantity": quantity,
                "purchase_price": float(purchase_price),
                "current_price": current_price,
                "unrealized_pnl": round(pnl, 2)
            }
            updated_positions.append(updated_pos)

    # Save new positions file for dashboard
    if updated_positions:
        save_positions(updated_positions)

    # Optionally log tick event to trading log (can customize for BUY/SELL)
    for position in positions:
        log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "ticker": position.get("ticker"),
            "action": "TICK_UPDATE",
            "quantity": position.get("quantity", ""),
            "price": current_prices.get(position.get("ticker")),
            "note": "Tick received"
        }
        append_to_trading_log(log_entry)

    return {
        "result": "success",
        "summary": {
            "positions_evaluated": positions_evaluated,
            "unrealized_pnl": unrealized_pnl
        },
        "decisions": []
    }

def get_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return []

def get_trading_log():
    if os.path.exists(TRADING_LOG_FILE):
        with open(TRADING_LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

def append_to_trading_log(entry):
    log = []
    if os.path.exists(TRADING_LOG_FILE):
        try:
            with open(TRADING_LOG_FILE, "r") as f:
                log = json.load(f)
        except Exception:
            log = []
    log.append(entry)
    with open(TRADING_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
