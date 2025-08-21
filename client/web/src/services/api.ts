import axios from 'axios';
import type { 
  User, 
  Stock, 
  Holding, 
  Transaction, 
  Fund, 
  WatchlistItem,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  TradeRequest
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (data: RegisterRequest) => {
    console.log('API: Sending registration request:', data);
    try {
      const response = await api.post('/api/auth/register', data);
      console.log('API: Registration response:', response.data);
      return response.data;
    } catch (error) {
      console.error('API: Registration error:', error);
      throw error;
    }
  },

  login: async (data: LoginRequest) => {
    console.log('API: Starting login request for:', data.username);
    try {
      const formData = new FormData();
      formData.append('username', data.username);
      formData.append('password', data.password);
      
      const response = await api.post<AuthResponse>('/api/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      console.log('API: Login response:', response.data);
      return response.data;
    } catch (error) {
      console.error('API: Login error:', error);
      throw error;
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/api/auth/logout');
    return response.data;
  }
};

// Stock API
export const stockAPI = {
  getAllStocks: async (): Promise<Stock[]> => {
    const response = await api.get<Stock[]>('/api/stocks/');
    return response.data;
  },

  searchStocks: async (query: string): Promise<Stock[]> => {
    const response = await api.get<Stock[]>(`/api/stocks/search?q=${query}`);
    return response.data;
  },

  getStockDetails: async (ticker: string): Promise<Stock> => {
    const response = await api.get<Stock>(`/api/stocks/${ticker}`);
    return response.data;
  }
};

// Portfolio API
export const portfolioAPI = {
  getHoldings: async (): Promise<Holding[]> => {
    const response = await api.get<Holding[]>('/api/portfolio/holdings');
    return response.data;
  },

  getTransactions: async (days: number = 30): Promise<Transaction[]> => {
    const response = await api.get<Transaction[]>(`/api/portfolio/transactions?days=${days}`);
    return response.data;
  },

  getFunds: async (): Promise<Fund> => {
    const response = await api.get<Fund>('/api/portfolio/funds/');
    return response.data;
  },

  addFunds: async (amount: number) => {
    const response = await api.post('/api/portfolio/funds/add', { amount });
    return response.data;
  },

  withdrawFunds: async (amount: number) => {
    const response = await api.post('/api/portfolio/funds/withdraw', { amount });
    return response.data;
  }
};

// Trading API
export const tradingAPI = {
  buyStock: async (data: TradeRequest) => {
    const response = await api.post('/api/trade/buy', data);
    return response.data;
  },

  sellStock: async (data: TradeRequest) => {
    const response = await api.post('/api/trade/sell', data);
    return response.data;
  }
};

// Watchlist API
export const watchlistAPI = {
  getWatchlist: async (): Promise<WatchlistItem[]> => {
    const response = await api.get<WatchlistItem[]>('/api/watchlist/');
    return response.data;
  },

  addToWatchlist: async (stockId: number) => {
    const response = await api.post('/api/watchlist/', { stock_id: stockId });
    return response.data;
  },

  removeFromWatchlist: async (stockId: number) => {
    const response = await api.delete(`/api/watchlist/${stockId}`);
    return response.data;
  }
};

// AI API
export const aiAPI = {
  getStockInsights: async (ticker: string) => {
    const response = await api.get(`/api/ai/stock-insights/${ticker}`);
    return response.data;
  },

  getMarketSentiment: async () => {
    const response = await api.get('/api/ai/market-sentiment');
    return response.data;
  },

  getPortfolioOverview: async () => {
    const response = await api.get('/api/ai/portfolio-overview');
    return response.data;
  }
};

export default api;
