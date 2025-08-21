import React, { useState, useEffect } from 'react';
import { Brain, TrendingUp, MessageSquare, BarChart3, Loader2, AlertCircle, Sparkles } from 'lucide-react';
import { aiAPI } from '../services/api';

interface StockInsight {
  ticker: string;
  company_name: string;
  current_price: number;
  insights: string;
  generated_at: string;
}

interface MarketSentiment {
  sentiment: 'positive' | 'negative' | 'neutral';
  sentiment_score: number;
  summary: string;
  news_count: number;
  analyzed_symbols: string[];
  generated_at: string;
}

interface PortfolioOverview {
  user_id: number;
  overview: string;
  generated_at: string;
}

const AIInsightsPage: React.FC = () => {
  const [marketSentiment, setMarketSentiment] = useState<MarketSentiment | null>(null);
  const [portfolioOverview, setPortfolioOverview] = useState<PortfolioOverview | null>(null);
  const [stockInsight, setStockInsight] = useState<StockInsight | null>(null);
  const [loading, setLoading] = useState({ sentiment: false, portfolio: false, stock: false });
  const [error, setError] = useState<string | null>(null);
  const [selectedStock, setSelectedStock] = useState('AAPL');

  const popularStocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'];

  const fetchMarketSentiment = async () => {
    setLoading(prev => ({ ...prev, sentiment: true }));
    setError(null);
    try {
      const data = await aiAPI.getMarketSentiment();
      setMarketSentiment(data);
    } catch (err) {
      setError('Failed to fetch market sentiment');
    } finally {
      setLoading(prev => ({ ...prev, sentiment: false }));
    }
  };

  const fetchPortfolioOverview = async () => {
    setLoading(prev => ({ ...prev, portfolio: true }));
    setError(null);
    try {
      const data = await aiAPI.getPortfolioOverview();
      setPortfolioOverview(data);
    } catch (err) {
      setError('Failed to fetch portfolio overview');
    } finally {
      setLoading(prev => ({ ...prev, portfolio: false }));
    }
  };

  const fetchStockInsight = async (ticker: string) => {
    setLoading(prev => ({ ...prev, stock: true }));
    setError(null);
    try {
      const data = await aiAPI.getStockInsights(ticker);
      setStockInsight(data);
      setSelectedStock(ticker);
    } catch (err) {
      setError('Failed to fetch stock insights');
    } finally {
      setLoading(prev => ({ ...prev, stock: false }));
    }
  };

  useEffect(() => {
    fetchMarketSentiment();
    fetchPortfolioOverview();
    fetchStockInsight(selectedStock);
  }, []);

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '📈';
      case 'negative': return '📉';
      default: return '📊';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-purple-600" />
            <h1 className="text-3xl font-bold text-gray-900">AI Insights</h1>
          </div>
          <span className="px-3 py-1 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-700 text-sm font-medium rounded-full flex items-center space-x-1">
            <Sparkles className="h-4 w-4" />
            <span>Powered by Groq</span>
          </span>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-red-500" />
          <span className="text-red-700">{error}</span>
          <button 
            onClick={() => setError(null)}
            className="ml-auto text-red-500 hover:text-red-700"
          >
            ×
          </button>
        </div>
      )}

      {/* Main AI Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Market Sentiment */}
        <div className="card">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <MessageSquare className="h-6 w-6 text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Market Sentiment</h2>
              </div>
              <button
                onClick={fetchMarketSentiment}
                disabled={loading.sentiment}
                className="btn btn-sm btn-secondary"
              >
                {loading.sentiment ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
              </button>
            </div>

            {marketSentiment ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{getSentimentIcon(marketSentiment.sentiment)}</span>
                  <div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(marketSentiment.sentiment)}`}>
                      {marketSentiment.sentiment.toUpperCase()}
                    </span>
                    <div className="text-sm text-gray-500 mt-1">
                      Score: {marketSentiment.sentiment_score.toFixed(2)}
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700 leading-relaxed">{marketSentiment.summary}</p>
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>Based on {marketSentiment.news_count} news sources</span>
                  <span>{marketSentiment.analyzed_symbols.length} stocks analyzed</span>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-32">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              </div>
            )}
          </div>
        </div>

        {/* Portfolio Analysis */}
        <div className="card">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-6 w-6 text-purple-600" />
                <h2 className="text-xl font-semibold text-gray-900">Portfolio Analysis</h2>
              </div>
              <button
                onClick={fetchPortfolioOverview}
                disabled={loading.portfolio}
                className="btn btn-sm btn-secondary"
              >
                {loading.portfolio ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
              </button>
            </div>

            {portfolioOverview ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-100 h-48 overflow-y-auto">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                    {portfolioOverview.overview}
                  </p>
                </div>
                <div className="text-xs text-gray-500">
                  Generated: {new Date(portfolioOverview.generated_at).toLocaleString()}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-32">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Stock Analysis */}
      <div className="card">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-6 w-6 text-green-600" />
              <h2 className="text-xl font-semibold text-gray-900">Stock Performance Analysis</h2>
            </div>
          </div>

          {/* Stock Selector */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select a stock to analyze:
            </label>
            <div className="flex flex-wrap gap-2">
              {popularStocks.map((stock) => (
                <button
                  key={stock}
                  onClick={() => fetchStockInsight(stock)}
                  disabled={loading.stock}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedStock === stock
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  } ${loading.stock ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {stock}
                </button>
              ))}
            </div>
          </div>

          {/* Stock Insight Display */}
          {stockInsight ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{stockInsight.ticker}</h3>
                  <p className="text-sm text-gray-600">{stockInsight.company_name}</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-gray-900">${stockInsight.current_price}</div>
                  <div className="text-sm text-gray-500">Current Price</div>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6 border border-green-100">
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-green-600" />
                  <span>AI Analysis</span>
                </h4>
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {stockInsight.insights}
                </p>
              </div>
              
              <div className="text-xs text-gray-500">
                Analysis generated: {new Date(stockInsight.generated_at).toLocaleString()}
              </div>
            </div>
          ) : loading.stock ? (
            <div className="flex items-center justify-center h-32">
              <div className="text-center">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400 mx-auto mb-2" />
                <p className="text-gray-500">Analyzing {selectedStock}...</p>
              </div>
            </div>
          ) : null}
        </div>
      </div>

      {/* AI Features Info */}
      <div className="card bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-100">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            <span>AI-Powered Features</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <MessageSquare className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h4 className="font-medium text-gray-900">Market Sentiment</h4>
              <p className="text-sm text-gray-600">Real-time sentiment analysis from news sources</p>
            </div>
            <div className="text-center">
              <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <h4 className="font-medium text-gray-900">Stock Insights</h4>
              <p className="text-sm text-gray-600">AI-powered performance analysis and predictions</p>
            </div>
            <div className="text-center">
              <BarChart3 className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <h4 className="font-medium text-gray-900">Portfolio Analysis</h4>
              <p className="text-sm text-gray-600">Personalized portfolio recommendations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsightsPage;
