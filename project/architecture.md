# Stock Web Application - System Architecture

This document outlines the system architecture for the stock trading web application.

**Technology Stack:**

*   **Frontend:** React
*   **Backend:** FastAPI
*   **Database:** PostgreSQL

---

## 1. Overall Architecture Flow

The application follows a classic three-tier architecture:

1.  **Frontend (React):** The user-facing application built with React. It is responsible for rendering the UI and handling user interactions. It communicates with the backend via RESTful API calls.

2.  **Backend (FastAPI):** The server-side application built with FastAPI. It handles business logic, user authentication, and data processing. It exposes a set of API endpoints for the frontend to consume.

3.  **Database (PostgreSQL):** A PostgreSQL database stores all the application data, including user information, stock data, transactions, and holdings.

**Flow Diagram:**

```
[Frontend (React)] <--> [Backend (FastAPI)] <--> [Database (PostgreSQL)]
      (API Calls)           (Database Queries)
```

---

## 2. Database Schema

The database schema is designed to store all the necessary information for the application to function.

### Users Table

Stores user account information.

| Column Name   | Data Type                | Constraints/Description          |
| :------------ | :----------------------- | :------------------------------- |
| user_id       | SERIAL                   | PRIMARY KEY                      |
| username      | VARCHAR(255)             | UNIQUE NOT NULL                  |
| email         | VARCHAR(255)             | UNIQUE NOT NULL                  |
| password_hash | VARCHAR(255)             | NOT NULL                         |
| created_at    | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP        |

### Stocks Table

Stores information about the stocks available for trading.

| Column Name   | Data Type      | Constraints/Description |
| :------------ | :------------- | :---------------------- |
| stock_id      | SERIAL         | PRIMARY KEY             |
| ticker_symbol | VARCHAR(10)    | UNIQUE NOT NULL         |
| company_name  | VARCHAR(255)   | NOT NULL                |
| current_price | NUMERIC(10, 2) | NOT NULL                |

### Holdings Table

Stores the stocks currently held by each user.

| Column Name  | Data Type      | Constraints/Description       |
| :----------- | :------------- | :---------------------------- |
| holding_id   | SERIAL         | PRIMARY KEY                   |
| user_id      | INTEGER        | FOREIGN KEY (Users.user_id)   |
| stock_id     | INTEGER        | FOREIGN KEY (Stocks.stock_id) |
| quantity     | INTEGER        | NOT NULL                      |
| average_cost | NUMERIC(10, 2) | NOT NULL                      |

### Watchlist Table

Stores the stocks that users are watching.

| Column Name  | Data Type | Constraints/Description       |
| :----------- | :-------- | :---------------------------- |
| watchlist_id | SERIAL    | PRIMARY KEY                   |
| user_id      | INTEGER   | FOREIGN KEY (Users.user_id)   |
| stock_id     | INTEGER   | FOREIGN KEY (Stocks.stock_id) |

### Transactions Table

Stores a record of all buy and sell transactions.

| Column Name        | Data Type                | Constraints/Description          |
| :----------------- | :----------------------- | :------------------------------- |
| transaction_id     | SERIAL                   | PRIMARY KEY                      |
| user_id            | INTEGER                  | FOREIGN KEY (Users.user_id)      |
| stock_id           | INTEGER                  | FOREIGN KEY (Stocks.stock_id)    |
| transaction_type   | VARCHAR(4)               | NOT NULL ('BUY' or 'SELL')      |
| quantity           | INTEGER                  | NOT NULL                         |
| price_per_share    | NUMERIC(10, 2)           | NOT NULL                         |
| transaction_date   | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP        |

### Funds Table

Stores the available funds for each user.

| Column Name | Data Type      | Constraints/Description     |
| :---------- | :------------- | :-------------------------- |
| fund_id     | SERIAL         | PRIMARY KEY                 |
| user_id     | INTEGER        | FOREIGN KEY (Users.user_id) |
| balance     | NUMERIC(15, 2) | NOT NULL                    |

---

## 3. API Layer (FastAPI)

The backend provides a RESTful API for the frontend. Here are the key endpoints:

*   **Authentication**
    *   `POST /api/auth/register`: Create a new user account.
    *   `POST /api/auth/login`: Authenticate a user and return a JWT token.

*   **Stocks**
    *   `GET /api/stocks`: Get a list of all available stocks.
    *   `GET /api/stocks/{ticker_symbol}`: Get detailed information for a specific stock.

*   **Watchlist**
    *   `GET /api/watchlist`: Get the current user's watchlist.
    *   `POST /api/watchlist`: Add a stock to the watchlist.
    *   `DELETE /api/watchlist/{stock_id}`: Remove a stock from the watchlist.

*   **Trading**
    *   `POST /api/trade/buy`: Place a buy order for a stock.
    *   `POST /api/trade/sell`: Place a sell order for a stock.

*   **Portfolio**
    *   `GET /api/portfolio/holdings`: Get the user's current stock holdings.
    *   `GET /api/portfolio/transactions`: Get the user's transaction history.
    *   `GET /api/portfolio/funds`: Get the user's current fund balance.
    *   `POST /api/portfolio/funds/add`: Add funds to the user's account.
    *   `POST /api/portfolio/funds/withdraw`: Withdraw funds from the user's account.