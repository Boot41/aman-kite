# Stock Web Application - End-to-End User Flow Specification

This document outlines the user flow and specifications for a stock trading web application.

**Technology Stack:**

*   **Frontend:** React
*   **Backend:** FastAPI
*   **Database:** PostgreSQL

---

## 1. User Stories & Workflow

The following user stories define the core functionalities of the application from a user's perspective.

*   **Login/Authentication:**
    *   As a new user, I want to be able to create an account.
    *   As an existing user, I want to be able to log in securely to my account.
    *   As a logged-in user, I want to be able to log out of my account.

*   **Dashboard & Portfolio:**
    *   As a logged-in user, I want to see a home dashboard that provides a quick overview of my portfolio performance.
    *   As a user, I want to be able to view a detailed list of my current stock holdings.
    *   As a user, I want to see my past transaction history (buy/sell orders).
    *   As a user, I want to be able to view my current funds and overall portfolio balance.

*   **Stock Information & Trading:**
    *   As a user, I want to be able to search for specific stocks.
    *   As a user, I want to view a detailed page for each stock, including its current price, historical data, and other relevant information.
    *   As a user, I want to be able to place buy and sell orders for stocks.


---

## 2. Page-by-Page Specifications

### 2.1. Login Page

*   **URL:** `/login`
*   **Elements:**
    *   Email/Username input field.
    *   Password input field.
    *   "Login" button.
    *   Link to the registration page ("Don't have an account? Sign up").
*   **Functionality:**
    *   Users can enter their credentials and click "Login".
    *   The backend will authenticate the user.
    *   Upon successful authentication, the user is redirected to the Home Dashboard.
    *   Error messages will be displayed for invalid credentials.

### 2.2. Home Dashboard

*   **URL:** `/` (or `/dashboard`)
*   **Elements:**
    *   **Header:** Navigation bar with links to Holdings, Transactions, Funds, and a Logout button.
    *   **Portfolio Summary:** A chart or graph showing the portfolio's performance over time (e.g., 1D, 1W, 1M, 1Y).
    *   **Holdings Snapshot:** A summarized view of the user's top holdings by value.
    *   **Watchlist:** A list of stocks the user is tracking.
    *   **Search Bar:** To search for stocks.
*   **Functionality:**
    *   The dashboard will fetch and display real-time data for the user's portfolio.
    *   The search bar will provide auto-suggestions as the user types.

### 2.3. Stock Details Page

*   **URL:** `/stocks/{ticker_symbol}` (e.g., `/stocks/GOOGL`)
*   **Elements:**
    *   **Stock Information:** Company name, ticker symbol, current price, and percentage change.
    *   **Interactive Chart:** A detailed chart showing historical price data with different time intervals.
    *   **Buy/Sell Controls:** Buttons to initiate buy or sell orders.
    *   **Company Profile:** A brief description of the company.
    *   **Market Depth:** Real-time bid and ask prices.
*   **Functionality:**
    *   This page will display comprehensive information for a selected stock.
    *   Users can interact with the chart to analyze historical performance.
    *   Clicking "Buy" or "Sell" will open a modal or a new page to place an order.

### 2.4. Holdings Page

*   **URL:** `/holdings`
*   **Elements:**
    *   A table listing all the stocks the user currently owns.
    *   **Columns:**
        *   Stock Name
        *   Ticker Symbol
        *   Quantity
        *   Average Cost
        *   Current Price
        *   Total Value
        *   Profit/Loss
*   **Functionality:**
    *   The data in the table will be updated in real-time.
    *   Users can sort the table by different columns.

### 2.5. Past Transactions Page

*   **URL:** `/transactions`
*   **Elements:**
    *   A table listing all past transactions.
    *   **Columns:**
        *   Date
        *   Stock Name
        *   Ticker Symbol
        *   Type (Buy/Sell)
        *   Quantity
        *   Price per Share
        *   Total Amount
*   **Functionality:**
    *   Users can filter transactions by date range or type.

### 2.6. Funds/Portfolio Balance Page

*   **URL:** `/funds`
*   **Elements:**
    *   **Available Funds:** The amount of cash available for trading.
    *   **Total Portfolio Value:** The sum of all holdings and available funds.
    *   **Add/Withdraw Funds:** Buttons to add or withdraw money from the account.
*   **Functionality:**
    *   Displays a clear breakdown of the user's financial status within the application.
