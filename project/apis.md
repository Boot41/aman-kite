# Stock Web Application - REST API Documentation

This document provides detailed documentation for the RESTful APIs used in the stock trading web application.

---

## 1. Authentication APIs

### 1.1. Register a New User

*   **Method:** `POST`
*   **Endpoint:** `/api/auth/register`
*   **Request Body:**

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

*   **Sample Response:**

```json
{
  "message": "User registered successfully"
}
```

### 1.2. Login

*   **Method:** `POST`
*   **Endpoint:** `/api/auth/login`
*   **Request Body:**

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

*   **Sample Response:**

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### 1.3. Logout

*   **Method:** `POST`
*   **Endpoint:** `/api/auth/logout`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "message": "Successfully logged out"
}
```

### 1.4. Get Current User Information

*   **Method:** `GET`
*   **Endpoint:** `/api/auth/me`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2023-10-27T10:00:00Z"
}
```

---

## 2. Stock Operations APIs

### 2.1. Search for a Stock

*   **Method:** `GET`
*   **Endpoint:** `/api/stocks/search?q={query}`
*   **Request Body:** None
*   **Sample Response:**

```json
[
  {
    "stock_id": 1,
    "ticker_symbol": "GOOGL",
    "company_name": "Alphabet Inc."
  },
  {
    "stock_id": 2,
    "ticker_symbol": "AAPL",
    "company_name": "Apple Inc."
  }
]
```

### 2.2. Get Stock Details

*   **Method:** `GET`
*   **Endpoint:** `/api/stocks/{ticker_symbol}`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "stock_id": 1,
  "ticker_symbol": "GOOGL",
  "company_name": "Alphabet Inc.",
  "current_price": 2800.00,
  "historical_data": { ... }
}
```

### 2.3. Add to Watchlist

*   **Method:** `POST`
*   **Endpoint:** `/api/watchlist`
*   **Request Body:**

```json
{
  "stock_id": 1
}
```

*   **Sample Response:**

```json
{
  "message": "Stock added to watchlist"
}
```

### 2.4. Remove from Watchlist

*   **Method:** `DELETE`
*   **Endpoint:** `/api/watchlist/{stock_id}`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "message": "Stock removed from watchlist"
}
```

### 2.5. Get All Stocks

*   **Method:** `GET`
*   **Endpoint:** `/api/stocks/`
*   **Request Body:** None
*   **Sample Response:**

```json
[
  {
    "stock_id": 1,
    "ticker_symbol": "GOOGL",
    "company_name": "Alphabet Inc.",
    "current_price": 2800.00,
    "last_updated": "2023-10-27T10:00:00Z"
  }
]
```

---

## 3. Holdings APIs

### 3.1. View Holdings

*   **Method:** `GET`
*   **Endpoint:** `/api/portfolio/holdings`
*   **Request Body:** None
*   **Sample Response:**

```json
[
  {
    "stock_id": 1,
    "ticker_symbol": "GOOGL",
    "quantity": 10,
    "average_cost": 2500.00,
    "current_price": 2800.00,
    "total_value": 28000.00
  }
]
```

### 3.2. Get Holding by Stock ID

*   **Method:** `GET`
*   **Endpoint:** `/api/portfolio/holdings/{stock_id}`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "stock_id": 1,
  "ticker_symbol": "GOOGL",
  "quantity": 10,
  "average_cost": 2500.00,
  "current_price": 2800.00,
  "total_value": 28000.00
}
```

### 3.3. Buy Stock

*   **Method:** `POST`
*   **Endpoint:** `/api/trade/buy`
*   **Request Body:**

```json
{
  "stock_id": 1,
  "quantity": 5
}
```

*   **Sample Response:**

```json
{
  "message": "Buy order successful"
}
```

### 3.4. Sell Stock

*   **Method:** `POST`
*   **Endpoint:** `/api/trade/sell`
*   **Request Body:**

```json
{
  "stock_id": 1,
  "quantity": 2
}
```

*   **Sample Response:**

```json
{
  "message": "Sell order successful"
}
```

---

## 4. Transactions API

### 4.1. View All Past Trades

*   **Method:** `GET`
*   **Endpoint:** `/api/portfolio/transactions`
*   **Request Body:** None
*   **Sample Response:**

```json
[
  {
    "transaction_id": 1,
    "stock_id": 1,
    "ticker_symbol": "GOOGL",
    "transaction_type": "BUY",
    "quantity": 10,
    "price_per_share": 2500.00,
    "transaction_date": "2023-10-27T10:00:00Z"
  }
]
```

---

## 5. Funds APIs

### 5.1. View Balance

*   **Method:** `GET`
*   **Endpoint:** `/api/portfolio/funds`
*   **Request Body:** None
*   **Sample Response:**

```json
{
  "balance": 50000.00
}
```

### 5.2. Add Funds

*   **Method:** `POST`
*   **Endpoint:** `/api/portfolio/funds/add`
*   **Request Body:**

```json
{
  "amount": 10000.00
}
```

*   **Sample Response:**

```json
{
  "message": "Funds added successfully"
}
```

### 5.3. Withdraw Funds

*   **Method:** `POST`
*   **Endpoint:** `/api/portfolio/funds/withdraw`
*   **Request Body:**

```json
{
  "amount": 5000.00
}
```

*   **Sample Response:**

```json
{
  "message": "Withdrawal successful"
}
```
