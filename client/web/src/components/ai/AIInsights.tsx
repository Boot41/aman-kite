import React, { useState, useEffect } from 'react';
import { Brain, TrendingUp, MessageSquare, BarChart3, Loader2, AlertCircle } from 'lucide-react';

interface AIInsightsProps {
  token: string;
}

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

const AIInsights: React.FC<AIInsightsProps> = ({ token }) => {
  const [marketSentiment, setMarketSentiment] = useState<MarketSentiment | null>(null);
  const [portfolioOverview, setPortfolioOverview] = useState<PortfolioOverview | null>(null);
  const [stockInsight, setStockInsight] = useState<StockInsight | null>(null);
  const [loading, setLoading] = useState({ sentiment: false, portfolio: false, stock: false });
  const [error, setError] = useState<string | null>(null);

  const API_BASE = 'http://localhost:8000';

  const fetchMarketSentiment = async () => {
    setLoading(prev => ({ ...prev, sentiment: true }));
    try {
      const response = await fetch(`${API_BASE}/api/ai/market-sentiment`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setMarketSentiment(data);
      }
    } catch (err) {
      setError('Failed to fetch market sentiment');
    } finally {
      setLoading(prev => ({ ...prev, sentiment: false }));
    }
  };

  const fetchPortfolioOverview = async () => {
    setLoading(prev => ({ ...prev, portfolio: true }));
    try {
      const response = await fetch(`${API_BASE}/api/ai/portfolio-overview`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setPortfolioOverview(data);
      }
    } catch (err) {
      setError('Failed to fetch portfolio overview');
    } finally {
      setLoading(prev => ({ ...prev, portfolio: false }));
    }
  };

  const fetchStockInsight = async (ticker: string = 'AAPL') => {
    setLoading(prev => ({ ...prev, stock: true }));
    try {
      const response = await fetch(`${API_BASE}/api/ai/stock-insights/${ticker}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setStockInsight(data);
      }
    } catch (err) {
      setError('Failed to fetch stock insights');
    } finally {
      setLoading(prev => ({ ...prev, stock: false }));
    }
  };

  useEffect(() => {
    fetchMarketSentiment();
    fetchPortfolioOverview();
    fetchStockInsight();
  }, [token]);

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
      {/* AI Insights Header */}
      <div className="flex items-center space-x-2 mb-6">
        <Brain className="h-6 w-6 text-purple-600" />
        <h2 className="text-2xl font-bold text-gray-900">AI Insights</h2>
        <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full">
          Powered by Groq
        </span>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-red-500" />
          <span className="text-red-700">{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* Market Sentiment */}
        <div className="card">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-900">Market Sentiment</h3>
              </div>
              {loading.sentiment && <Loader2 className="h-4 w-4 animate-spin text-gray-400" />}
            </div>

            {marketSentiment ? (
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">{getSentimentIcon(marketSentiment.sentiment)}</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(marketSentiment.sentiment)}`}>
                    {marketSentiment.sentiment.toUpperCase()}
                  </span>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-sm text-gray-700">{marketSentiment.summary}</p>
                </div>
                <div className="text-xs text-gray-500">
                  Based on {marketSentiment.news_count} news sources
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-24">
                <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
              </div>
            )}
          </div>
        </div>

        {/* Stock Insights */}
        <div className="card">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <h3 className="text-lg font-semibold text-gray-900">Stock Analysis</h3>
              </div>
              {loading.stock && <Loader2 className="h-4 w-4 animate-spin text-gray-400" />}
            </div>

            {stockInsight ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-gray-900">{stockInsight.ticker}</div>
                    <div className="text-sm text-gray-500">{stockInsight.company_name}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-gray-900">${stockInsight.current_price}</div>
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-sm text-gray-700">{stockInsight.insights}</p>
                </div>
                <button
                  onClick={() => fetchStockInsight('MSFT')}
                  className="text-xs text-blue-600 hover:text-blue-700"
                >
                  Analyze different stock →
                </button>
              </div>
            ) : (
              <div className="flex items-center justify-center h-24">
                <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
              </div>
            )}
          </div>
        </div>

        {/* Portfolio Overview */}
        <div className="card lg:col-span-2 xl:col-span-1">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-purple-600" />
                <h3 className="text-lg font-semibold text-gray-900">Portfolio Analysis</h3>
              </div>
              {loading.portfolio && <Loader2 className="h-4 w-4 animate-spin text-gray-400" />}
            </div>

            {portfolioOverview ? (
              <div className="space-y-3">
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {portfolioOverview.overview}
                  </p>
                </div>
                <button
                  onClick={fetchPortfolioOverview}
                  className="text-xs text-purple-600 hover:text-purple-700"
                >
                  Refresh analysis →
                </button>
              </div>
            ) : (
              <div className="flex items-center justify-center h-24">
                <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Actions */}
      <div className="card">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Actions</h3>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={fetchMarketSentiment}
              disabled={loading.sentiment}
              className="btn btn-secondary flex items-center space-x-2"
            >
              {loading.sentiment ? <Loader2 className="h-4 w-4 animate-spin" /> : <MessageSquare className="h-4 w-4" />}
              <span>Refresh Sentiment</span>
            </button>
            <button
              onClick={fetchPortfolioOverview}
              disabled={loading.portfolio}
              className="btn btn-secondary flex items-center space-x-2"
            >
              {loading.portfolio ? <Loader2 className="h-4 w-4 animate-spin" /> : <BarChart3 className="h-4 w-4" />}
              <span>Analyze Portfolio</span>
            </button>
            <button
              onClick={() => fetchStockInsight('GOOGL')}
              disabled={loading.stock}
              className="btn btn-secondary flex items-center space-x-2"
            >
              {loading.stock ? <Loader2 className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />}
              <span>Stock Insights</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsights;
