import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  TrendingUp, 
  TrendingDown, 
  Star, 
  StarOff,
  ShoppingCart,
  DollarSign
} from 'lucide-react';
import { stockAPI, tradingAPI, watchlistAPI, portfolioAPI } from '../services/api';
import type { Stock, Fund } from '../types';

const StockDetails: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [stock, setStock] = useState<Stock | null>(null);
  const [funds, setFunds] = useState<Fund | null>(null);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [tradeType, setTradeType] = useState<'buy' | 'sell'>('buy');
  const [quantity, setQuantity] = useState(1);
  const [isTrading, setIsTrading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchStockData = async () => {
      if (!ticker) return;

      try {
        const [stockData, fundsData, watchlistData] = await Promise.all([
          stockAPI.getStockDetails(ticker),
          portfolioAPI.getFunds(),
          watchlistAPI.getWatchlist()
        ]);

        setStock(stockData);
        setFunds(fundsData);
        setIsInWatchlist(watchlistData.some(item => item.ticker_symbol === ticker));
      } catch (error) {
        console.error('Error fetching stock data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStockData();
  }, [ticker]);

  const handleWatchlistToggle = async () => {
    if (!stock) return;

    try {
      if (isInWatchlist) {
        await watchlistAPI.removeFromWatchlist(stock.stock_id);
        setIsInWatchlist(false);
        setMessage('Removed from watchlist');
      } else {
        await watchlistAPI.addToWatchlist(stock.stock_id);
        setIsInWatchlist(true);
        setMessage('Added to watchlist');
      }
      setTimeout(() => setMessage(''), 3000);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error updating watchlist');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const handleTrade = async () => {
    if (!stock) return;

    setIsTrading(true);
    try {
      if (tradeType === 'buy') {
        await tradingAPI.buyStock({ stock_id: stock.stock_id, quantity });
        setMessage(`Successfully bought ${quantity} shares of ${stock.ticker_symbol}`);
      } else {
        await tradingAPI.sellStock({ stock_id: stock.stock_id, quantity });
        setMessage(`Successfully sold ${quantity} shares of ${stock.ticker_symbol}`);
      }
      
      // Refresh funds data
      const updatedFunds = await portfolioAPI.getFunds();
      setFunds(updatedFunds);
      
      setTimeout(() => setMessage(''), 5000);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Trade failed');
      setTimeout(() => setMessage(''), 5000);
    } finally {
      setIsTrading(false);
    }
  };

  const totalCost = stock ? stock.current_price * quantity : 0;
  const canAfford = funds ? funds.balance >= totalCost : false;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!stock) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Stock not found</h2>
        <Link to="/dashboard" className="btn btn-primary">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Link to="/dashboard" className="p-2 hover:bg-gray-100 rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-900">{stock.ticker_symbol}</h1>
          <p className="text-gray-600">{stock.company_name}</p>
        </div>
        <button
          onClick={handleWatchlistToggle}
          className="p-2 hover:bg-gray-100 rounded-full"
        >
          {isInWatchlist ? (
            <Star className="h-6 w-6 text-yellow-500 fill-current" />
          ) : (
            <StarOff className="h-6 w-6 text-gray-400" />
          )}
        </button>
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

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stock Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Price Card */}
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-4xl font-bold text-gray-900">
                  ${stock.current_price.toFixed(2)}
                </p>
                {stock.historical_data && (
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`flex items-center space-x-1 ${
                      stock.historical_data.change >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {stock.historical_data.change >= 0 ? (
                        <TrendingUp className="h-4 w-4" />
                      ) : (
                        <TrendingDown className="h-4 w-4" />
                      )}
                      <span>
                        {stock.historical_data.change >= 0 ? '+' : ''}
                        ${stock.historical_data.change.toFixed(2)} 
                        ({stock.historical_data.change_percent.toFixed(2)}%)
                      </span>
                    </span>
                  </div>
                )}
              </div>
            </div>
            <p className="text-sm text-gray-500">
              Last updated: {new Date(stock.last_updated).toLocaleString()}
            </p>
          </div>

          {/* Company Info */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Company Information</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Symbol</span>
                <span className="font-medium">{stock.ticker_symbol}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Company Name</span>
                <span className="font-medium">{stock.company_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Current Price</span>
                <span className="font-medium">${stock.current_price.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Trading Panel */}
        <div className="space-y-6">
          {/* Available Funds */}
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="bg-blue-100 p-2 rounded-full">
                <DollarSign className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Available Funds</p>
                <p className="text-xl font-bold text-gray-900">
                  ${funds?.balance.toFixed(2) || '0.00'}
                </p>
              </div>
            </div>
            <Link to="/funds" className="btn btn-secondary w-full">
              Add Funds
            </Link>
          </div>

          {/* Trading Form */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Trade</h3>
            
            {/* Trade Type Toggle */}
            <div className="flex rounded-lg bg-gray-100 p-1 mb-4">
              <button
                onClick={() => setTradeType('buy')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  tradeType === 'buy'
                    ? 'bg-success-600 text-white'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                Buy
              </button>
              <button
                onClick={() => setTradeType('sell')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  tradeType === 'sell'
                    ? 'bg-danger-600 text-white'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                Sell
              </button>
            </div>

            {/* Quantity Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quantity
              </label>
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                className="input"
              />
            </div>

            {/* Order Summary */}
            <div className="bg-gray-50 p-4 rounded-lg mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-600">Price per share</span>
                <span className="font-medium">${stock.current_price.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-600">Quantity</span>
                <span className="font-medium">{quantity}</span>
              </div>
              <div className="border-t border-gray-200 pt-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-900">Total</span>
                  <span className="font-bold text-lg">${totalCost.toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Trade Button */}
            <button
              onClick={handleTrade}
              disabled={isTrading || (tradeType === 'buy' && !canAfford)}
              className={`btn w-full flex items-center justify-center space-x-2 ${
                tradeType === 'buy' ? 'btn-success' : 'btn-danger'
              } ${(isTrading || (tradeType === 'buy' && !canAfford)) ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <ShoppingCart className="h-4 w-4" />
              <span>
                {isTrading 
                  ? 'Processing...' 
                  : `${tradeType === 'buy' ? 'Buy' : 'Sell'} ${quantity} Share${quantity > 1 ? 's' : ''}`
                }
              </span>
            </button>

            {tradeType === 'buy' && !canAfford && (
              <p className="text-sm text-danger-600 mt-2">
                Insufficient funds. You need ${(totalCost - (funds?.balance || 0)).toFixed(2)} more.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockDetails;
