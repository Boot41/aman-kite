import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Briefcase, TrendingUp, TrendingDown, ExternalLink } from 'lucide-react';
import { portfolioAPI } from '../services/api';
import type { Holding } from '../types';

const Holdings: React.FC = () => {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchHoldings = async () => {
      try {
        const data = await portfolioAPI.getHoldings();
        setHoldings(data);
      } catch (error) {
        console.error('Error fetching holdings:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHoldings();
  }, []);

  const totalValue = holdings.reduce((sum, holding) => sum + holding.total_value, 0);
  const totalProfitLoss = holdings.reduce((sum, holding) => sum + holding.profit_loss, 0);

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
        <h1 className="text-3xl font-bold text-gray-900">Holdings</h1>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Value</p>
              <p className="text-2xl font-bold text-gray-900">${totalValue.toFixed(2)}</p>
            </div>
            <div className="bg-primary-100 p-3 rounded-full">
              <Briefcase className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total P&L</p>
              <p className={`text-2xl font-bold ${totalProfitLoss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                ${totalProfitLoss.toFixed(2)}
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

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Stocks</p>
              <p className="text-2xl font-bold text-gray-900">{holdings.length}</p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <Briefcase className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Your Holdings</h2>
        </div>
        <div className="overflow-x-auto">
          {holdings.length > 0 ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stock
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Cost
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Current Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Value
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    P&L
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {holdings.map((holding) => (
                  <tr key={holding.holding_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{holding.ticker_symbol}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      {holding.quantity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      ${holding.average_cost.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      ${holding.current_price.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      ${holding.total_value.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`font-medium ${holding.profit_loss >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                        {holding.profit_loss >= 0 ? '+' : ''}${holding.profit_loss.toFixed(2)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link
                        to={`/stocks/${holding.ticker_symbol}`}
                        className="text-primary-600 hover:text-primary-900 flex items-center space-x-1"
                      >
                        <span>Trade</span>
                        <ExternalLink className="h-4 w-4" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-12">
              <Briefcase className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No holdings yet</h3>
              <p className="text-gray-500 mb-6">Start trading to build your portfolio</p>
              <Link to="/dashboard" className="btn btn-primary">
                Explore Stocks
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Holdings;
