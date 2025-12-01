import json
import os
import requests
from datetime import datetime
from ai_integration import get_chatgpt_analysis
from config import MAKE_TRADE_API_KEY, MAKE_TRADE_URL

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSITIONS_FILE = os.path.join(CURRENT_DIR, "Assignment6PositionsSample.txt")
TRADING_LOG_FILE = os.path.join(CURRENT_DIR, "Assignment6TradingLogSample.txt")

def analyze_tick_payload(payload, tick_id):
    """
    Analyzes tick payload, gets AI recommendations, and posts to make_trade.
    
    Args:
        payload: The tick payload with positions and market data
        tick_id: Unique identifier for this tick
    
    Returns:
        Response dict with result, summary, and decisions
    """
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
    
    # Log tick event to trading log
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
    
    # Get ChatGPT recommendations
    decisions = []
    try:
        ai_recommendations = get_chatgpt_analysis(payload)
        decisions = ai_recommendations
        
        # Log AI recommendations to trading log
        for decision in ai_recommendations:
            log_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "ticker": decision.get("ticker"),
                "action": decision.get("action"),
                "quantity": decision.get("quantity", 0),
                "price": current_prices.get(decision.get("ticker"), "N/A"),
                "note": f"AI recommendation from ChatGPT"
            }
            append_to_trading_log(log_entry)
        
        # Post to make_trade endpoint
        if ai_recommendations:
            make_trade_response = post_to_make_trade(tick_id, ai_recommendations)
            if make_trade_response and "Positions" in make_trade_response:
                # Update positions with the response from make_trade
                new_positions = make_trade_response.get("Positions", [])
                save_positions(new_positions)
    
    except Exception as e:
        print(f"[ERROR] AI analysis failed: {str(e)}")
        # Continue without AI if it fails
        pass
    
    return {
        "result": "success",
        "summary": {
            "positions_evaluated": positions_evaluated,
            "unrealized_pnl": round(unrealized_pnl, 2)
        },
        "decisions": decisions
    }


def post_to_make_trade(tick_id, trades):
    """
    Posts trade recommendations to the make_trade endpoint.
    
    Args:
        tick_id: Unique identifier for this tick
        trades: List of trade recommendations
    
    Returns:
        Response JSON from make_trade endpoint or None
    """
    if not MAKE_TRADE_API_KEY:
        print("[WARNING] MAKE_TRADE_API_KEY not configured, skipping make_trade call")
        return None
    
    payload = {
        "id": tick_id,
        "trades": trades
    }
    
    headers = {
        "x-api-key": MAKE_TRADE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(MAKE_TRADE_URL, json=payload, headers=headers, timeout=30)
        print(f"[DEBUG] make_trade response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[DEBUG] make_trade response: {result}")
            return result
        else:
            print(f"[ERROR] make_trade returned status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to post to make_trade: {str(e)}")
        return None


def get_positions():
    """Retrieve current positions from file."""
    if os.path.exists(POSITIONS_FILE):
        try:
            with open(POSITIONS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load positions: {str(e)}")
            return []
    return []


def get_trading_log():
    """Retrieve trading log from file."""
    if os.path.exists(TRADING_LOG_FILE):
        try:
            with open(TRADING_LOG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load trading log: {str(e)}")
            return []
    return []


def save_positions(positions):
    """Save positions to file."""
    try:
        with open(POSITIONS_FILE, "w") as f:
            json.dump(positions, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save positions: {str(e)}")


def append_to_trading_log(entry):
    """Append entry to trading log file."""
    log = []
    if os.path.exists(TRADING_LOG_FILE):
        try:
            with open(TRADING_LOG_FILE, "r") as f:
                log = json.load(f)
        except Exception:
            log = []
    
    log.append(entry)
    
    try:
        with open(TRADING_LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to append to trading log: {str(e)}")
