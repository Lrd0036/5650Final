def validate_tick_payload(data):
    """
    Validates the tick payload structure and required fields.
    Returns (True, None) if valid, otherwise (False, error_message).
    """
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object"
    
    # Check Positions key, allow both "Positions" and "positions"
    if "Positions" in data:
        positions = data.get("Positions")
    elif "positions" in data:
        positions = data.get("positions")
    else:
        return False, "Missing required field: Positions"
    
    # Check Market Summary key, allow multiple variants
    if "MarketSummary" in data:
        market_summary = data.get("MarketSummary")
    elif "Market_Summary" in data:
        market_summary = data.get("Market_Summary")
    elif "marketSummary" in data:
        market_summary = data.get("marketSummary")
    else:
        return False, "Missing required field: MarketSummary"
    
    # Validate Positions
    if not isinstance(positions, list):
        return False, "Positions must be a list"
    if len(positions) == 0:
        return False, "Positions must be a non-empty list"
    
    for pos in positions:
        if not isinstance(pos, dict):
            return False, "Each position must be an object"
        
        # Accept 'ticker', 'quantity', 'purchaseprice' or 'purchase_price'
        if "ticker" not in pos or "quantity" not in pos or not ("purchaseprice" in pos or "purchase_price" in pos):
            return False, "Position missing required fields (ticker, quantity, purchaseprice)"
        
        try:
            float(pos["quantity"])
            if "purchaseprice" in pos:
                float(pos["purchaseprice"])
            else:
                float(pos["purchase_price"])
        except (ValueError, TypeError):
            return False, "Position quantity and purchaseprice must be numeric"
    
    # Validate Market Summary
    if not isinstance(market_summary, list):
        return False, "Market Summary must be a list"
    if len(market_summary) == 0:
        return False, "Market Summary must be a non-empty list"
    
    for summary in market_summary:
        if not isinstance(summary, dict):
            return False, "Each market summary entry must be an object"
        
        # Accept 'ticker' and either 'currentprice' or 'current_price'
        if "ticker" not in summary or not ("currentprice" in summary or "current_price" in summary):
            return False, "Market summary missing required fields (ticker, currentprice)"
        
        try:
            if "currentprice" in summary:
                float(summary["currentprice"])
            else:
                float(summary["current_price"])
        except (ValueError, TypeError):
            return False, "Market summary currentprice must be numeric"
    
    return True, None
