#!/usr/bin/env python3
"""
API Testing Script for Stock Trading Application
Tests all endpoints to ensure they're working properly
"""

import requests
import json
import sys
import pytest

# This file is a manual integration script that expects a running server.
# Skip it during automated pytest runs to avoid fixture errors and external calls.
pytestmark = pytest.mark.skip(reason="Integration script; requires running server on localhost:8000")

BASE_URL = "http://localhost:8000"

def test_basic_endpoints():
    """Test basic health endpoints"""
    print("=== Testing Basic Endpoints ===")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"GET / - Status: {response.status_code}, Response: {response.json()}")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"GET /health - Status: {response.status_code}, Response: {response.json()}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    
    # Test user registration
    user_data = {
        "username": "apitest",
        "email": "apitest@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"POST /api/auth/register - Status: {response.status_code}, Response: {response.json()}")
    
    # Test user login
    login_data = {
        "username": "apitest@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print(f"POST /api/auth/login - Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Login successful! Token type: {token_data['token_type']}")
        token = token_data["access_token"]
        
        # Test get current user info
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"GET /api/auth/me - Status: {response.status_code}, Response: {response.json()}")
        
        return token
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_stock_endpoints():
    """Test stock-related endpoints"""
    print("\n=== Testing Stock Endpoints ===")
    
    # Test get all stocks
    response = requests.get(f"{BASE_URL}/api/stocks/")
    print(f"GET /api/stocks/ - Status: {response.status_code}, Response: {response.json()}")
    
    # Test search stocks
    response = requests.get(f"{BASE_URL}/api/stocks/search?q=Apple")
    print(f"GET /api/stocks/search?q=Apple - Status: {response.status_code}, Response: {response.json()}")
    
    # Test get stock details (this might fail if no stocks exist)
    response = requests.get(f"{BASE_URL}/api/stocks/AAPL")
    print(f"GET /api/stocks/AAPL - Status: {response.status_code}, Response: {response.json()}")

def test_portfolio_endpoints(token):
    """Test portfolio-related endpoints"""
    print("\n=== Testing Portfolio Endpoints ===")
    
    if not token:
        print("No token available, skipping authenticated tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get user funds
    response = requests.get(f"{BASE_URL}/api/portfolio/funds/", headers=headers)
    print(f"GET /api/portfolio/funds/ - Status: {response.status_code}, Response: {response.json()}")
    
    # Test add funds
    response = requests.post(f"{BASE_URL}/api/portfolio/funds/add", 
                           json={"amount": 1000.00}, headers=headers)
    print(f"POST /api/portfolio/funds/add - Status: {response.status_code}, Response: {response.json()}")
    
    # Test get holdings
    response = requests.get(f"{BASE_URL}/api/portfolio/holdings", headers=headers)
    print(f"GET /api/portfolio/holdings - Status: {response.status_code}, Response: {response.json()}")
    
    # Test get transactions
    response = requests.get(f"{BASE_URL}/api/portfolio/transactions", headers=headers)
    print(f"GET /api/portfolio/transactions - Status: {response.status_code}, Response: {response.json()}")

def test_watchlist_endpoints(token):
    """Test watchlist endpoints"""
    print("\n=== Testing Watchlist Endpoints ===")
    
    if not token:
        print("No token available, skipping authenticated tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get watchlist
    response = requests.get(f"{BASE_URL}/api/watchlist/", headers=headers)
    print(f"GET /api/watchlist/ - Status: {response.status_code}, Response: {response.json()}")

def test_trading_endpoints(token):
    """Test trading endpoints"""
    print("\n=== Testing Trading Endpoints ===")
    
    if not token:
        print("No token available, skipping authenticated tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test buy stock (this will likely fail without stocks in DB)
    buy_data = {"stock_id": 1, "quantity": 5}
    response = requests.post(f"{BASE_URL}/api/trade/buy", json=buy_data, headers=headers)
    print(f"POST /api/trade/buy - Status: {response.status_code}, Response: {response.json()}")
    
    # Test sell stock (this will likely fail without holdings)
    sell_data = {"stock_id": 1, "quantity": 2}
    response = requests.post(f"{BASE_URL}/api/trade/sell", json=sell_data, headers=headers)
    print(f"POST /api/trade/sell - Status: {response.status_code}, Response: {response.json()}")

def main():
    """Run all API tests"""
    print("Starting API Testing...")
    
    try:
        # Test basic endpoints
        test_basic_endpoints()
        
        # Test authentication and get token
        token = test_auth_endpoints()
        
        # Test stock endpoints
        test_stock_endpoints()
        
        # Test portfolio endpoints
        test_portfolio_endpoints(token)
        
        # Test watchlist endpoints
        test_watchlist_endpoints(token)
        
        # Test trading endpoints
        test_trading_endpoints(token)
        
        print("\n=== API Testing Complete ===")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running on http://localhost:8000")
        sys.exit(1)
    except Exception as e:
        print(f"Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
