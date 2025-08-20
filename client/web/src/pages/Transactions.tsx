import React, { useState, useEffect } from 'react';
import { History, ArrowUpRight, ArrowDownRight, Filter } from 'lucide-react';
import { portfolioAPI } from '../services/api';
import type { Transaction } from '../types';

const Transactions: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [filteredTransactions, setFilteredTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<'ALL' | 'BUY' | 'SELL'>('ALL');
  const [days, setDays] = useState(30);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const data = await portfolioAPI.getTransactions(days);
        setTransactions(data);
        setFilteredTransactions(data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransactions();
  }, [days]);

  useEffect(() => {
    if (filter === 'ALL') {
      setFilteredTransactions(transactions);
    } else {
      setFilteredTransactions(transactions.filter(t => t.transaction_type === filter));
    }
  }, [filter, transactions]);

  const totalBuyValue = transactions
    .filter(t => t.transaction_type === 'BUY')
    .reduce((sum, t) => sum + (t.quantity * t.price_per_share), 0);

  const totalSellValue = transactions
    .filter(t => t.transaction_type === 'SELL')
    .reduce((sum, t) => sum + (t.quantity * t.price_per_share), 0);

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
        <h1 className="text-3xl font-bold text-gray-900">Transaction History</h1>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Transactions</p>
              <p className="text-2xl font-bold text-gray-900">{transactions.length}</p>
            </div>
            <div className="bg-primary-100 p-3 rounded-full">
              <History className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Bought</p>
              <p className="text-2xl font-bold text-success-600">${totalBuyValue.toFixed(2)}</p>
            </div>
            <div className="bg-success-100 p-3 rounded-full">
              <ArrowUpRight className="h-6 w-6 text-success-600" />
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Sold</p>
              <p className="text-2xl font-bold text-danger-600">${totalSellValue.toFixed(2)}</p>
            </div>
            <div className="bg-danger-100 p-3 rounded-full">
              <ArrowDownRight className="h-6 w-6 text-danger-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <Filter className="h-5 w-5 text-gray-400" />
            <div className="flex space-x-2">
              {['ALL', 'BUY', 'SELL'].map((type) => (
                <button
                  key={type}
                  onClick={() => setFilter(type as 'ALL' | 'BUY' | 'SELL')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    filter === type
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-600">Last</label>
            <select
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value))}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm"
            >
              <option value={7}>7 days</option>
              <option value={30}>30 days</option>
              <option value={90}>90 days</option>
              <option value={365}>1 year</option>
            </select>
          </div>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Transactions ({filteredTransactions.length})
          </h2>
        </div>
        <div className="overflow-x-auto">
          {filteredTransactions.length > 0 ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stock
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTransactions.map((transaction) => (
                  <tr key={transaction.transaction_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(transaction.transaction_date).toLocaleDateString()}
                      <div className="text-xs text-gray-500">
                        {new Date(transaction.transaction_date).toLocaleTimeString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <div className={`p-1 rounded-full ${
                          transaction.transaction_type === 'BUY' ? 'bg-success-100' : 'bg-danger-100'
                        }`}>
                          {transaction.transaction_type === 'BUY' ? (
                            <ArrowUpRight className="h-3 w-3 text-success-600" />
                          ) : (
                            <ArrowDownRight className="h-3 w-3 text-danger-600" />
                          )}
                        </div>
                        <span className={`text-sm font-medium ${
                          transaction.transaction_type === 'BUY' ? 'text-success-600' : 'text-danger-600'
                        }`}>
                          {transaction.transaction_type}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{transaction.ticker_symbol}</div>
                      <div className="text-sm text-gray-500">{transaction.company_name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {transaction.quantity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${transaction.price_per_share.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ${(transaction.quantity * transaction.price_per_share).toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-12">
              <History className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No transactions found</h3>
              <p className="text-gray-500">
                {filter === 'ALL' 
                  ? 'Your transaction history will appear here' 
                  : `No ${filter.toLowerCase()} transactions in the selected period`
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Transactions;
