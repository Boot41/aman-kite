import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Star, TrendingUp, TrendingDown, Trash2, ExternalLink, Search } from 'lucide-react';
import { watchlistAPI, stockAPI } from '../services/api';
import type { WatchlistItem, Stock } from '../types';

const Watchlist: React.FC = () => {
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [allStocks, setAllStocks] = useState<Stock[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredStocks, setFilteredStocks] = useState<Stock[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (searchQuery) {
      const filtered = allStocks.filter(stock => 
        !watchlist.some(w => w.stock_id === stock.stock_id) &&
        (stock.ticker_symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
         stock.company_name.toLowerCase().includes(searchQuery.toLowerCase()))
      );
      setFilteredStocks(filtered.slice(0, 10)); // Limit to 10 results
    } else {
      setFilteredStocks([]);
    }
  }, [searchQuery, allStocks, watchlist]);

  const fetchData = async () => {
    try {
      const [watchlistData, stocksData] = await Promise.all([
        watchlistAPI.getWatchlist(),
        stockAPI.getAllStocks()
      ]);
      setWatchlist(watchlistData);
      setAllStocks(stocksData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddToWatchlist = async (stockId: number) => {
    setIsAdding(true);
    try {
      await watchlistAPI.addToWatchlist(stockId);
      await fetchData(); // Refresh data
      setMessage('Stock added to watchlist');
      setSearchQuery(''); // Clear search
      setTimeout(() => setMessage(''), 3000);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error adding to watchlist');
      setTimeout(() => setMessage(''), 3000);
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemoveFromWatchlist = async (stockId: number) => {
    try {
      await watchlistAPI.removeFromWatchlist(stockId);
      await fetchData(); // Refresh data
      setMessage('Stock removed from watchlist');
      setTimeout(() => setMessage(''), 3000);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error removing from watchlist');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Watchlist</h1>
      </div>

      {/* Message */}
      {message && (
        <div className={`p-4 rounded-md ${
          message.includes('Error') || message.includes('failed')
            ? 'bg-danger-50 text-danger-700 border border-danger-200' 
            : 'bg-success-50 text-success-700 border border-success-200'
        }`}>
          {message}
        </div>
      )}

      {/* Add Stock Section */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Add Stock to Watchlist</h2>
        
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-10"
            placeholder="Search stocks by symbol or company name..."
          />
        </div>

        {/* Search Results */}
        {filteredStocks.length > 0 && (
          <div className="mt-4 border border-gray-200 rounded-lg divide-y divide-gray-200">
            {filteredStocks.map((stock) => (
              <div key={stock.stock_id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                <div>
                  <p className="font-medium text-gray-900">{stock.ticker_symbol}</p>
                  <p className="text-sm text-gray-500">{stock.company_name}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="font-medium text-gray-900">${stock.current_price.toFixed(2)}</p>
                    {stock.historical_data && (
                      <p className={`text-sm ${
                        stock.historical_data.change >= 0 ? 'text-success-600' : 'text-danger-600'
                      }`}>
                        {stock.historical_data.change >= 0 ? '+' : ''}
                        {stock.historical_data.change_percent.toFixed(2)}%
                      </p>
                    )}
                  </div>
                  <button
                    onClick={() => handleAddToWatchlist(stock.stock_id)}
                    disabled={isAdding}
                    className="btn btn-primary btn-sm flex items-center space-x-1"
                  >
                    <Star className="h-4 w-4" />
                    <span>Add</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Watchlist */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Your Watchlist ({watchlist.length})
          </h2>
        </div>
        
        {watchlist.length > 0 ? (
          <div className="divide-y divide-gray-200">
            {watchlist.map((item) => {
              const stock = allStocks.find(s => s.stock_id === item.stock_id);
              return (
                <div key={item.watchlist_id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="bg-yellow-100 p-2 rounded-full">
                        <Star className="h-5 w-5 text-yellow-600 fill-current" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{item.ticker_symbol}</h3>
                        <p className="text-sm text-gray-500">{item.company_name}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-6">
                      <div className="text-right">
                        <p className="text-lg font-semibold text-gray-900">
                          ${item.current_price.toFixed(2)}
                        </p>
                        {stock?.historical_data && (
                          <div className="flex items-center space-x-1">
                            {stock.historical_data.change >= 0 ? (
                              <TrendingUp className="h-4 w-4 text-success-600" />
                            ) : (
                              <TrendingDown className="h-4 w-4 text-danger-600" />
                            )}
                            <span className={`text-sm ${
                              stock.historical_data.change >= 0 ? 'text-success-600' : 'text-danger-600'
                            }`}>
                              {stock.historical_data.change >= 0 ? '+' : ''}
                              {stock.historical_data.change_percent.toFixed(2)}%
                            </span>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Link
                          to={`/stocks/${item.ticker_symbol}`}
                          className="btn btn-primary btn-sm flex items-center space-x-1"
                        >
                          <ExternalLink className="h-4 w-4" />
                          <span>Trade</span>
                        </Link>
                        <button
                          onClick={() => handleRemoveFromWatchlist(item.stock_id)}
                          className="btn btn-secondary btn-sm p-2"
                          title="Remove from watchlist"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <Star className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Your watchlist is empty</h3>
            <p className="text-gray-500 mb-6">Add stocks you're interested in to track their performance</p>
            <div className="text-sm text-gray-400">
              Use the search box above to find and add stocks to your watchlist
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Watchlist;
