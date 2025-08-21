#!/usr/bin/env python3
"""Test AI endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_ai_endpoints():
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
    
    print("=== Testing AI Endpoints ===")
    
    # Test stock insights
    response = requests.get(f"{BASE_URL}/api/ai/stock-insights/AAPL", headers=headers)
    print(f"Stock Insights: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Ticker: {data['ticker']}")
        print(f"  Insights: {data['insights'][:100]}...")
    else:
        print(f"  Error: {response.text}")
    
    # Test market sentiment
    response = requests.get(f"{BASE_URL}/api/ai/market-sentiment", headers=headers)
    print(f"Market Sentiment: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Sentiment: {data['sentiment']}")
        print(f"  Summary: {data['summary'][:100]}...")
    else:
        print(f"  Error: {response.text}")
    
    # Test portfolio overview
    response = requests.get(f"{BASE_URL}/api/ai/portfolio-overview", headers=headers)
    print(f"Portfolio Overview: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Overview: {data['overview'][:100]}...")
    else:
        print(f"  Error: {response.text}")

if __name__ == "__main__":
    test_ai_endpoints()
