#!/usr/bin/env python3
"""
Test the fixed trading APIs and complete watchlist testing
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    # Login with existing user
    login_data = {
        "username": "apitest@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_fixed_trading_apis():
    """Test the fixed trading APIs"""
    print("=== Testing Fixed Trading APIs ===")
    
    token = get_auth_token()
    if not token:
        print("Failed to get auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test buy stock with correct schema
    buy_data = {"stock_id": 1, "quantity": 2}
    response = requests.post(f"{BASE_URL}/api/trade/buy", json=buy_data, headers=headers)
    print(f"POST /api/trade/buy - Status: {response.status_code}, Response: {response.json()}")
    
    # Check holdings after buy
    response = requests.get(f"{BASE_URL}/api/portfolio/holdings", headers=headers)
    print(f"GET /api/portfolio/holdings (after buy) - Status: {response.status_code}, Response: {response.json()}")
    
    # Check funds after buy
    response = requests.get(f"{BASE_URL}/api/portfolio/funds/", headers=headers)
    print(f"GET /api/portfolio/funds/ (after buy) - Status: {response.status_code}, Response: {response.json()}")
    
    # Test sell stock
    sell_data = {"stock_id": 1, "quantity": 1}
    response = requests.post(f"{BASE_URL}/api/trade/sell", json=sell_data, headers=headers)
    print(f"POST /api/trade/sell - Status: {response.status_code}, Response: {response.json()}")
    
    # Check holdings after sell
    response = requests.get(f"{BASE_URL}/api/portfolio/holdings", headers=headers)
    print(f"GET /api/portfolio/holdings (after sell) - Status: {response.status_code}, Response: {response.json()}")
    
    # Check transactions
    response = requests.get(f"{BASE_URL}/api/portfolio/transactions", headers=headers)
    print(f"GET /api/portfolio/transactions - Status: {response.status_code}, Response: {response.json()}")

def test_watchlist_operations():
    """Test watchlist add/remove operations"""
    print("\n=== Testing Watchlist Operations ===")
    
    token = get_auth_token()
    if not token:
        print("Failed to get auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add stock to watchlist
    watchlist_data = {"stock_id": 1}
    response = requests.post(f"{BASE_URL}/api/watchlist/", json=watchlist_data, headers=headers)
    print(f"POST /api/watchlist/ (add) - Status: {response.status_code}, Response: {response.json()}")
    
    # Get watchlist
    response = requests.get(f"{BASE_URL}/api/watchlist/", headers=headers)
    print(f"GET /api/watchlist/ (after add) - Status: {response.status_code}, Response: {response.json()}")
    
    # Try to add same stock again (should fail)
    response = requests.post(f"{BASE_URL}/api/watchlist/", json=watchlist_data, headers=headers)
    print(f"POST /api/watchlist/ (duplicate) - Status: {response.status_code}, Response: {response.json()}")
    
    # Remove from watchlist
    response = requests.delete(f"{BASE_URL}/api/watchlist/1", headers=headers)
    print(f"DELETE /api/watchlist/1 - Status: {response.status_code}, Response: {response.json()}")
    
    # Get watchlist after removal
    response = requests.get(f"{BASE_URL}/api/watchlist/", headers=headers)
    print(f"GET /api/watchlist/ (after remove) - Status: {response.status_code}, Response: {response.json()}")

def main():
    """Run the additional tests"""
    print("Testing Fixed APIs...")
    
    try:
        test_fixed_trading_apis()
        test_watchlist_operations()
        print("\n=== Additional API Testing Complete ===")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
