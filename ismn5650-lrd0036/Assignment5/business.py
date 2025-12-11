def analyze_tick_payload(payload):
    # Robustly get Positions (allowing "Positions" or "positions")
    positions = payload.get("Positions", payload.get("positions", []))

    # Robustly get Market Summary (allowing "MarketSummary", "Market_Summary", or "marketSummary")
    if "MarketSummary" in payload:
        market_summary = payload.get("MarketSummary")
    elif "Market_Summary" in payload:
        market_summary = payload.get("Market_Summary")
    else:
        market_summary = payload.get("marketSummary", [])

    current_prices = {}
    for item in market_summary:
        ticker = item.get("ticker")
        # Check for current_price with or without underscore
        current_price = item.get("currentprice", item.get("current_price"))
        if ticker and current_price is not None:
            current_prices[ticker] = float(current_price)

    unrealized_pnl = 0.0
    positions_evaluated = 0

    for position in positions:
        ticker = position.get("ticker")
        quantity = float(position.get("quantity", 0))
        # Check purchase_price with or without underscore
        purchase_price = position.get("purchaseprice", position.get("purchase_price"))
        if ticker in current_prices and purchase_price is not None:
            current_price = current_prices[ticker]
            # PnL = (current_price - purchase_price) * quantity
            pnl = (current_price - float(purchase_price)) * quantity
            unrealized_pnl += pnl
            positions_evaluated += 1

    return {
        "result": "success",
        "summary": {
            # FIXED: Keys must include underscores to match the tester/requirement
            "positions_evaluated": positions_evaluated,
            "unrealized_pnl": unrealized_pnl
        },
        "decisions": []
    }