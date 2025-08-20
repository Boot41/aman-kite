
const BASE_URL = 'http://localhost:8000';

/**
 * Retrieves the authentication token from localStorage.
 * @returns {string | null} The authentication token or null if not found.
 */
const getAuthToken = (): string | null => {
    return localStorage.getItem('authToken');
};

/**
 * A helper function to make authenticated API requests.
 * @param {string} endpoint The API endpoint to call.
 * @param {RequestInit} options The options for the fetch request.
 * @returns {Promise<any>} A promise that resolves to the JSON response.
 */
const apiFetch = async (endpoint: string, options: RequestInit = {}): Promise<any> => {
    const token = getAuthToken();
    const headers = new Headers(options.headers);

    if (!headers.has('Content-Type') && options.body) {
        headers.set('Content-Type', 'application/json');
    }

    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Something went wrong');
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
};

// --- Auth APIs ---

export const register = (data: any) => {
    return apiFetch('/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
    });
};

export const login = async (data: any) => {
    const responseData = await apiFetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data),
    });

    if (responseData.access_token) {
        localStorage.setItem('authToken', responseData.access_token);
    }
    return responseData;
};

export const logout = async () => {
    const response = await apiFetch('/auth/logout', {
        method: 'POST',
    });
    localStorage.removeItem('authToken');
    return response;
};

export const getCurrentUser = () => {
    return apiFetch('/auth/me');
};

// --- Stocks APIs ---

export const getAllStocks = () => {
    return apiFetch('/stocks/');
};

export const searchStocks = (query: string) => {
    return apiFetch(`/stocks/search?query=${query}`);
};

export const getStockDetails = (tickerSymbol: string) => {
    return apiFetch(`/stocks/${tickerSymbol}`);
};

// --- Funds APIs ---

export const getUserFunds = () => {
    return apiFetch('/funds/');
};

export const addFunds = (amount: number) => {
    return apiFetch('/funds/add', {
        method: 'POST',
        body: JSON.stringify({ amount }),
    });
};

export const withdrawFunds = (amount: number) => {
    return apiFetch('/funds/withdraw', {
        method: 'POST',
        body: JSON.stringify({ amount }),
    });
};

// --- Holdings APIs ---

export const getUserHoldings = () => {
    return apiFetch('/holdings/');
};

export const getHoldingByStock = (stockId: number) => {
    return apiFetch(`/holdings/${stockId}`);
};

// --- Transactions APIs ---

export const getUserTransactions = (days: number = 30) => {
    return apiFetch(`/transactions/?days=${days}`);
};

export const buyStock = (data: { stock_id: number; quantity: number }) => {
    return apiFetch('/transactions/buy', {
        method: 'POST',
        body: JSON.stringify(data),
    });
};

export const sellStock = (data: { stock_id: number; quantity: number }) => {
    return apiFetch('/transactions/sell', {
        method: 'POST',
        body: JSON.stringify(data),
    });
};

// --- Watchlist APIs ---

export const getUserWatchlist = () => {
    return apiFetch('/watchlist/');
};

export const addToWatchlist = (stockId: number) => {
    return apiFetch('/watchlist/', {
        method: 'POST',
        body: JSON.stringify({ stock_id: stockId }),
    });
};

export const removeFromWatchlist = (stockId: number) => {
    return apiFetch(`/watchlist/${stockId}`, {
        method: 'DELETE',
    });
};
