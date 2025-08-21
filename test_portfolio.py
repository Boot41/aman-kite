#!/usr/bin/env python3
"""Test the new portfolio endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_portfolio_endpoints():
    # Login to get token
    login_data = {
        "username": "apitest@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code != 200:
        print("Login failed")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add more funds
    response = requests.post(f"{BASE_URL}/api/portfolio/funds/add", 
                           json={"amount": 5000.00}, headers=headers)
    print(f"Add funds: {response.status_code} - {response.json()}")
    
    # Buy some stock
    response = requests.post(f"{BASE_URL}/api/trade/buy", 
                           json={"stock_id": 1, "quantity": 10}, headers=headers)
    print(f"Buy stock: {response.status_code} - {response.json()}")
    
    # Test current value endpoint
    response = requests.get(f"{BASE_URL}/api/portfolio/current-value", headers=headers)
    print(f"Current value: {response.status_code} - {response.text}")
    if response.text:
        print(f"Current value JSON: {response.json()}")
    
    # Test refresh prices endpoint
    response = requests.post(f"{BASE_URL}/api/portfolio/refresh-prices", headers=headers)
    print(f"Refresh prices: {response.status_code} - {response.json()}")
    
    # Test current value again after refresh
    response = requests.get(f"{BASE_URL}/api/portfolio/current-value", headers=headers)
    print(f"Current value after refresh: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_portfolio_endpoints()
