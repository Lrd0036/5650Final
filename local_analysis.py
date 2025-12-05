import json
from datetime import datetime, timedelta

def get_simulated_growth(positions):
    """
    Calculates the initial non-CASH portfolio value and simulates a 10-day 
    growth curve using deterministic, slightly volatile data.
    
    Args:
        positions (list): List of current position dictionaries.
        
    Returns:
        list: Array of {"date": "Day X", "value": X.XX} for the line chart.
    """
    
    # 1. Calculate Initial Value (Total Market Value excluding CASH)
    initial_value = sum(
        pos.get('quantity', 0) * pos.get('purchase_price', 0)
        for pos in positions if pos.get('ticker') != 'CASH'
    )
    
    # Use a minimum value if portfolio is empty to prevent crashes
    if initial_value == 0:
        initial_value = 1000.00
        
    growth_data = []
    current_value = initial_value
    
    # Start the simulation from the current date (Day 0)
    start_date = datetime.now()
    
    # 2. Simulate 10 days of growth
    for day in range(11): # Days 0 through 10
        date_label = (start_date + timedelta(days=day)).strftime("Day %d")
        
        # Apply a daily change factor: 0.1% base growth +/- 1.5% volatility
        # Note: Volatility is slightly aggressive for demonstration purposes
        daily_growth_factor = 1.001 + (random.uniform(-0.015, 0.015))
        
        # Day 0 is the starting value
        if day > 0:
            current_value *= daily_growth_factor
            
        growth_data.append({
            "date": date_label,
            "value": round(current_value, 2)
        })

    return growth_data

import random