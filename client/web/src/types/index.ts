// API Types
export interface User {
  user_id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

export interface Stock {
  stock_id: number;
  ticker_symbol: string;
  company_name: string;
  current_price: number;
  last_updated: string;
  historical_data?: {
    price: number;
    change: number;
    change_percent: number;
  };
}

export interface Holding {
  holding_id: number;
  user_id: number;
  stock_id: number;
  quantity: number;
  average_cost: number;
  ticker_symbol: string;
  current_price: number;
  total_value: number;
  profit_loss: number;
}

export interface Transaction {
  transaction_id: number;
  user_id: number;
  stock_id: number;
  transaction_type: 'BUY' | 'SELL';
  quantity: number;
  price_per_share: number;
  transaction_date: string;
  ticker_symbol: string;
  company_name: string;
}

export interface Fund {
  user_id: number;
  balance: number;
}

export interface WatchlistItem {
  watchlist_id: number;
  user_id: number;
  stock_id: number;
  ticker_symbol: string;
  company_name: string;
  current_price: number;
}

// Auth Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Trade Types
export interface TradeRequest {
  stock_id: number;
  quantity: number;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  detail?: string;
}
