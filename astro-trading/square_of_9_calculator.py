#!/usr/bin/env python3
"""
Gann Square of 9 Calculator for Bitcoin
Converts BTC price to degrees for planetary timing analysis
"""

import math
import json
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_square_of_9(center_value, size=50):
    """
    Generate Square of 9 spiral with given center value
    Returns dict: {price: degree}
    """
    square = {}
    
    # Start at center
    x, y = 0, 0
    value = center_value
    degree = 0
    
    square[value] = degree
    
    # Spiral outward
    for ring in range(1, size):
        # Move to start of ring (right edge)
        x += 1
        value += 1
        degree = (degree + 45) % 360  # Each ring adds 45°
        
        # Go around the ring
        directions = [
            (0, 1),   # Up
            (-1, 0),  # Left  
            (0, -1),  # Down
            (1, 0)    # Right
        ]
        
        side_length = 2 * ring
        
        for direction in directions:
            dx, dy = direction
            for step in range(side_length):
                if step > 0:  # Don't double-count corners
                    value += 1
                    degree = (degree + (360 / (8 * ring))) % 360
                    square[value] = degree
                x += dx
                y += dy
    
    return square

def price_to_degree(price, square_dict):
    """
    Convert BTC price to degree using Square of 9
    Uses closest value if exact match not found
    """
    if price in square_dict:
        return square_dict[price]
    
    # Find closest price
    closest_price = min(square_dict.keys(), key=lambda x: abs(x - price))
    return square_dict[closest_price]

def calculate_planetary_price_targets(current_price, planetary_degrees):
    """
    Given current BTC price and upcoming planetary aspects (in degrees),
    calculate potential price targets using Square of 9
    """
    # Generate square around current price
    square = generate_square_of_9(int(current_price), size=100)
    
    targets = {}
    for planet_aspect, degree in planetary_degrees.items():
        # Find prices that correspond to this degree (±5°)
        matching_prices = []
        for price, price_degree in square.items():
            if abs(price_degree - degree) <= 5:
                matching_prices.append(price)
        
        if matching_prices:
            targets[planet_aspect] = {
                'degree': degree,
                'prices': sorted(matching_prices),
                'closest_to_current': min(matching_prices, key=lambda x: abs(x - current_price))
            }
    
    return targets

def analyze_btc_square_levels(current_price=100000):
    """
    Analyze key Square of 9 levels around current BTC price
    """
    print(f"Square of 9 Analysis for BTC at ${current_price:,}")
    print("=" * 50)
    
    # Generate square centered on current price
    square = generate_square_of_9(int(current_price), size=30)
    
    # Sort by price
    sorted_prices = sorted(square.keys())
    
    print("\nKey Price Levels and Their Degrees:")
    print("Price\t\tDegree")
    print("-" * 25)
    
    for price in sorted_prices:
        if abs(price - current_price) <= current_price * 0.2:  # Within ±20%
            degree = square[price]
            print(f"${price:,}\t\t{degree:.1f}°")
    
    return square

def find_geometric_relationships(square_dict, price_levels):
    """
    Find geometric relationships between key price levels
    """
    relationships = {}
    
    for i, price1 in enumerate(price_levels):
        if price1 not in square_dict:
            continue
            
        for price2 in price_levels[i+1:]:
            if price2 not in square_dict:
                continue
                
            degree1 = square_dict[price1]
            degree2 = square_dict[price2]
            
            angle_diff = abs(degree2 - degree1)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            # Check for key geometric angles
            key_angles = [30, 45, 60, 90, 120, 135, 150, 180]
            for angle in key_angles:
                if abs(angle_diff - angle) <= 3:  # Within 3°
                    relationships[f"${price1:,} to ${price2:,}"] = {
                        'angle': angle,
                        'actual_diff': angle_diff,
                        'ratio': price2 / price1
                    }
                    break
    
    return relationships

if __name__ == "__main__":
    print("Gann Square of 9 Calculator for Bitcoin")
    print("=======================================\n")
    
    # Current BTC price (approximate)
    current_btc = 100000
    
    # Analyze current levels
    square = analyze_btc_square_levels(current_btc)
    
    # Key historical BTC levels to analyze
    key_levels = [
        69000,   # Previous ATH
        15500,   # 2022 bottom
        100000,  # Current level
        150000,  # Potential target
        200000,  # Extended target
    ]
    
    print(f"\n\nGeometric Relationships Between Key Levels:")
    print("=" * 50)
    
    relationships = find_geometric_relationships(square, key_levels)
    
    for relationship, data in relationships.items():
        print(f"{relationship}: {data['angle']}° angle, {data['ratio']:.2f}x ratio")
    
    # Example planetary degrees for March 2026
    march_planetary_degrees = {
        'Mars-Jupiter Trine': 120,      # Mar 21
        'Saturn-Neptune Conj': 30,      # Feb 20 extended influence  
        'Mars-Saturn Conj': 180,        # Apr 18
        'Lunar Eclipse': 90,            # Mar 3
    }
    
    print(f"\n\nPotential Price Targets from Planetary Aspects:")
    print("=" * 50)
    
    targets = calculate_planetary_price_targets(current_btc, march_planetary_degrees)
    
    for aspect, data in targets.items():
        closest = data['closest_to_current']
        direction = "↑" if closest > current_btc else "↓"
        change_pct = ((closest - current_btc) / current_btc) * 100
        
        print(f"{aspect} ({data['degree']}°): ${closest:,} {direction} ({change_pct:+.1f}%)")
        
        # Show all targets within range
        nearby_targets = [p for p in data['prices'] if abs(p - current_btc) <= current_btc * 0.3]
        if len(nearby_targets) > 1:
            print(f"  Other targets: {', '.join([f'${p:,}' for p in nearby_targets if p != closest])}")