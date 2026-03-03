#!/usr/bin/env python3
"""
Bitcoin Square of 9 Calculator
Clean, focused tool for BTC price-to-degree analysis
"""

import math
import json
from datetime import datetime, timedelta

def generate_btc_square(center_price, max_rings=25):
    """
    Generate Square of 9 for Bitcoin with realistic price ranges
    Returns dict: {price: degree}
    """
    square = {}
    
    # Start at center
    price = int(center_price)
    degree = 0
    square[price] = degree
    
    # Spiral outward
    for ring in range(1, max_rings + 1):
        # Each ring has 8 * ring positions
        ring_positions = 8 * ring
        degree_increment = 360 / ring_positions
        
        # Calculate price increment for this ring
        # Use different increments based on price range
        if center_price < 50000:
            price_increment = ring * 100  # $100 per ring position for lower prices
        elif center_price < 100000:
            price_increment = ring * 200  # $200 per ring position for mid prices
        else:
            price_increment = ring * 500  # $500 per ring position for higher prices
        
        # Generate positions in this ring
        for pos in range(ring_positions):
            price += price_increment
            degree = (degree + degree_increment) % 360
            square[price] = degree
    
    return square

def find_price_targets_by_degree(square, target_degrees, tolerance=3):
    """
    Find Bitcoin prices that correspond to specific degrees
    """
    targets = {}
    
    for desc, target_deg in target_degrees.items():
        matching_prices = []
        
        for price, degree in square.items():
            # Check if degree matches (accounting for 0°/360° wraparound)
            diff1 = abs(degree - target_deg)
            diff2 = abs(degree - (target_deg + 360))
            diff3 = abs((degree + 360) - target_deg)
            
            min_diff = min(diff1, diff2, diff3)
            
            if min_diff <= tolerance:
                matching_prices.append(price)
        
        if matching_prices:
            targets[desc] = sorted(matching_prices)
    
    return targets

def analyze_btc_current_position(current_price):
    """
    Analyze current BTC position in Square of 9
    """
    # Generate square around current price
    square = generate_btc_square(current_price)
    
    # Find current degree
    current_degree = None
    closest_price = min(square.keys(), key=lambda x: abs(x - current_price))
    current_degree = square[closest_price]
    
    print(f"BTC Square of 9 Analysis")
    print(f"Current Price: ${current_price:,}")
    print(f"Nearest Square Price: ${closest_price:,}")
    print(f"Current Degree: {current_degree:.1f}°")
    print("=" * 50)
    
    return square, current_degree

def get_key_planetary_degrees():
    """
    Return key planetary aspects and their degrees for March 2026
    """
    return {
        'Mars-Jupiter Trine (Bullish)': 120,
        'Saturn-Neptune Conj (Transformation)': 30,
        'Mars-Saturn Conj (Bearish)': 180,
        'Lunar Eclipse (Volatility)': 90,
        'Sun-Mars Square (Tension)': 90,
        'Venus-Jupiter Trine (Growth)': 120,
        'Mercury-Saturn Opposition (Resistance)': 180,
        'Full Moon (Reversal)': 180,
    }

def show_key_support_resistance(square, current_price, range_pct=0.15):
    """
    Show key Square of 9 levels within range as support/resistance
    """
    price_range = current_price * range_pct
    min_price = current_price - price_range
    max_price = current_price + price_range
    
    relevant_levels = []
    for price, degree in square.items():
        if min_price <= price <= max_price:
            # Focus on key degrees (multiples of 30°, 45°, 90°)
            if any(abs(degree - key_deg) <= 2 for key_deg in [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]):
                relevant_levels.append((price, degree))
    
    relevant_levels.sort()
    
    print(f"\nKey Square of 9 Levels (±{range_pct*100:.0f}% range):")
    print("Price\t\tDegree\t\tLevel Type")
    print("-" * 45)
    
    for price, degree in relevant_levels:
        if degree in [0, 180]:
            level_type = "Major S/R"
        elif degree in [90, 270]:
            level_type = "Turn Point"
        elif degree in [45, 135, 225, 315]:
            level_type = "Breakout"
        else:
            level_type = "Support"
        
        change_pct = ((price - current_price) / current_price) * 100
        direction = "↑" if price > current_price else "↓"
        
        print(f"${price:,}\t{degree:.0f}°\t\t{level_type} {direction} ({change_pct:+.1f}%)")

def main():
    # Current BTC price (approximate)
    current_btc = 100000
    
    # Analyze current position
    square, current_degree = analyze_btc_current_position(current_btc)
    
    # Show key levels for trading
    show_key_support_resistance(square, current_btc)
    
    # Get planetary targets
    planetary_degrees = get_key_planetary_degrees()
    targets = find_price_targets_by_degree(square, planetary_degrees, tolerance=5)
    
    print(f"\n\nPlanetary Price Targets (March 2026):")
    print("=" * 50)
    
    for aspect, prices in targets.items():
        if prices:
            # Find closest target to current price
            closest_target = min(prices, key=lambda x: abs(x - current_btc))
            change_pct = ((closest_target - current_btc) / current_btc) * 100
            direction = "🟢" if change_pct > 0 else "🔴"
            
            print(f"{aspect}")
            print(f"  Primary Target: ${closest_target:,} {direction} ({change_pct:+.1f}%)")
            
            # Show 1-2 alternative targets if they exist
            other_targets = [p for p in prices[:3] if p != closest_target and abs(p - current_btc) < current_btc * 0.3]
            if other_targets:
                alt_str = ", ".join([f"${p:,}" for p in other_targets[:2]])
                print(f"  Alternatives: {alt_str}")
            print()
    
    print("\n📈 **Trading Notes:**")
    print("• Major S/R (0°/180°): Strong support/resistance")
    print("• Turn Points (90°/270°): High probability reversals")  
    print("• Breakout levels (45°/135°/225°/315°): Momentum continuation")
    print("• Watch for planetary aspect dates to activate these levels")

if __name__ == "__main__":
    main()