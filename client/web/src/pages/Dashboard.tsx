import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Briefcase, 
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Plus,
  Brain,
  Sparkles
} from 'lucide-react';
import { portfolioAPI, stockAPI } from '../services/api';
import type { Holding, Fund, Transaction, Stock } from '../types';

const Dashboard: React.FC = () => {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [funds, setFunds] = useState<Fund | null>(null);
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [topStocks, setTopStocks] = useState<Stock[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [holdingsData, fundsData, transactionsData, stocksData] = await Promise.all([
          portfolioAPI.getHoldings(),
          portfolioAPI.getFunds(),
          portfolioAPI.getTransactions(7), // Last 7 days
          stockAPI.getAllStocks()
        ]);

        setHoldings(holdingsData);
        setFunds(fundsData);
        setRecentTransactions(transactionsData.slice(0, 5)); // Show only 5 recent
        setTopStocks(stocksData.slice(0, 6)); // Show top 6 stocks
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const totalPortfolioValue = holdings.reduce((sum, holding) => sum + holding.total_value, 0);
  const totalProfitLoss = holdings.reduce((sum, holding) => sum + holding.profit_loss, 0);
  const profitLossPercentage = totalPortfolioValue > 0 ? (totalProfitLoss / (totalPortfolioValue - totalProfitLoss)) * 100 : 0;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <Link
          to="/funds"
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Funds</span>
        </Link>
      </div>

      {/* Portfolio Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Portfolio</p>
              <p className="text-2xl font-bold text-gray-900">
                ${(totalPortfolioValue + (funds?.balance || 0)).toFixed(2)}
              </p>
            </div>
            <div className="bg-primary-100 p-3 rounded-full">
              <Briefcase className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Invested Value</p>
              <p className="text-2xl font-bold text-gray-900">
                ${totalPortfolioValue.toFixed(2)}
              </p>
            </div>
            <div className="bg-success-100 p-3 rounded-full">
              <TrendingUp className="h-6 w-6 text-success-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Available Funds</p>
              <p className="text-2xl font-bold text-gray-900">
                ${funds?.balance.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">P&L</p>
              <p className={`text-2xl font-bold ${totalProfitLoss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                ${totalProfitLoss.toFixed(2)}
              </p>
              <p className={`text-sm ${totalProfitLoss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {profitLossPercentage >= 0 ? '+' : ''}{profitLossPercentage.toFixed(2)}%
              </p>
            </div>
            <div className={`p-3 rounded-full ${totalProfitLoss >= 0 ? 'bg-success-100' : 'bg-danger-100'}`}>
              {totalProfitLoss >= 0 ? (
                <TrendingUp className="h-6 w-6 text-success-600" />
              ) : (
                <TrendingDown className="h-6 w-6 text-danger-600" />
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Holdings Overview */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Top Holdings</h2>
              <Link to="/holdings" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                View all
              </Link>
            </div>
          </div>
          <div className="p-6">
            {holdings.length > 0 ? (
              <div className="space-y-4">
                {holdings.slice(0, 5).map((holding) => (
                  <div key={holding.holding_id} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{holding.ticker_symbol}</p>
                      <p className="text-sm text-gray-500">{holding.quantity} shares</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-gray-900">${holding.total_value.toFixed(2)}</p>
                      <p className={`text-sm ${holding.profit_loss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                        {holding.profit_loss >= 0 ? '+' : ''}${holding.profit_loss.toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No holdings yet</p>
                <p className="text-sm text-gray-400">Start trading to see your portfolio here</p>
              </div>
            )}
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
              <Link to="/transactions" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                View all
              </Link>
            </div>
          </div>
          <div className="p-6">
            {recentTransactions.length > 0 ? (
              <div className="space-y-4">
                {recentTransactions.map((transaction) => (
                  <div key={transaction.transaction_id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-full ${
                        transaction.transaction_type === 'BUY' ? 'bg-success-100' : 'bg-danger-100'
                      }`}>
                        {transaction.transaction_type === 'BUY' ? (
                          <ArrowUpRight className="h-4 w-4 text-success-600" />
                        ) : (
                          <ArrowDownRight className="h-4 w-4 text-danger-600" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">
                          {transaction.transaction_type} {transaction.ticker_symbol}
                        </p>
                        <p className="text-sm text-gray-500">
                          {transaction.quantity} shares at ${transaction.price_per_share}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-gray-900">
                        ${(transaction.quantity * transaction.price_per_share).toFixed(2)}
                      </p>
                      <p className="text-sm text-gray-500">
                        {new Date(transaction.transaction_date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No recent activity</p>
                <p className="text-sm text-gray-400">Your transactions will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Insights Preview */}
      <div className="card bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-100">
        <div className="p-6 border-b border-purple-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="h-6 w-6 text-purple-600" />
              <h2 className="text-lg font-semibold text-gray-900">AI Insights</h2>
              <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full flex items-center space-x-1">
                <Sparkles className="h-3 w-3" />
                <span>New</span>
              </span>
            </div>
            <Link to="/ai-insights" className="text-purple-600 hover:text-purple-700 text-sm font-medium">
              View all insights →
            </Link>
          </div>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-white rounded-lg border border-purple-100">
              <div className="text-2xl mb-2">📈</div>
              <h4 className="font-medium text-gray-900 mb-1">Market Sentiment</h4>
              <p className="text-sm text-gray-600">AI-powered sentiment analysis</p>
            </div>
            <div className="text-center p-4 bg-white rounded-lg border border-purple-100">
              <div className="text-2xl mb-2">🧠</div>
              <h4 className="font-medium text-gray-900 mb-1">Stock Analysis</h4>
              <p className="text-sm text-gray-600">Performance insights & predictions</p>
            </div>
            <div className="text-center p-4 bg-white rounded-lg border border-purple-100">
              <div className="text-2xl mb-2">📊</div>
              <h4 className="font-medium text-gray-900 mb-1">Portfolio Review</h4>
              <p className="text-sm text-gray-600">Personalized recommendations</p>
            </div>
          </div>
        </div>
      </div>

      {/* Market Overview */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Market Overview</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {topStocks.map((stock) => (
              <Link
                key={stock.stock_id}
                to={`/stocks/${stock.ticker_symbol}`}
                className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-gray-900">{stock.ticker_symbol}</p>
                    <p className="text-sm text-gray-500 truncate">{stock.company_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">${stock.current_price}</p>
                    {stock.historical_data && (
                      <p className={`text-sm ${
                        stock.historical_data.change >= 0 ? 'text-success-600' : 'text-danger-600'
                      }`}>
                        {stock.historical_data.change >= 0 ? '+' : ''}
                        {stock.historical_data.change_percent.toFixed(2)}%
                      </p>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
