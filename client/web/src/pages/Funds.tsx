import React, { useState, useEffect } from 'react';
import { DollarSign, Plus, Minus, CreditCard, Wallet } from 'lucide-react';
import { portfolioAPI } from '../services/api';
import type { Fund } from '../types';

const Funds: React.FC = () => {
  const [funds, setFunds] = useState<Fund | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [amount, setAmount] = useState('');
  const [operation, setOperation] = useState<'add' | 'withdraw'>('add');
  const [isProcessing, setIsProcessing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchFunds();
  }, []);

  const fetchFunds = async () => {
    try {
      const data = await portfolioAPI.getFunds();
      setFunds(data);
    } catch (error: unknown) {
      console.error('Error fetching funds:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTransaction = async (e: React.FormEvent) => {
    e.preventDefault();
    const transactionAmount = parseFloat(amount);
    
    if (!transactionAmount || transactionAmount <= 0) {
      setMessage('Please enter a valid amount');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    if (operation === 'withdraw' && funds && transactionAmount > funds.balance) {
      setMessage('Insufficient funds for withdrawal');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    setIsProcessing(true);
    try {
      if (operation === 'add') {
        await portfolioAPI.addFunds(transactionAmount);
        setMessage(`Successfully added ${transactionAmount.toFixed(2)} to your account`);
      } else {
        await portfolioAPI.withdrawFunds(transactionAmount);
        setMessage(`Successfully withdrew ${transactionAmount.toFixed(2)} from your account`);
      }
      
      setAmount('');
      await fetchFunds(); // Refresh funds data
      setTimeout(() => setMessage(''), 5000);
    } catch (error: unknown) {
      const err = error as any;
      setMessage(err.response?.data?.detail || 'Transaction failed');
      setTimeout(() => setMessage(''), 5000);
    } finally {
      setIsProcessing(false);
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
        <h1 className="text-3xl font-bold text-gray-900">Funds Management</h1>
      </div>

      {/* Message */}
      {message && (
        <div className={`p-4 rounded-md ${
          message.includes('Error') || message.includes('failed') || message.includes('Insufficient')
            ? 'bg-danger-50 text-danger-700 border border-danger-200' 
            : 'bg-success-50 text-success-700 border border-success-200'
        }`}>
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Current Balance */}
        <div className="lg:col-span-1">
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-sm font-medium text-gray-600">Available Balance</p>
                <p className="text-3xl font-bold text-gray-900">
                  ${funds?.balance.toFixed(2) || '0.00'}
                </p>
              </div>
              <div className="bg-primary-100 p-3 rounded-full">
                <Wallet className="h-8 w-8 text-primary-600" />
              </div>
            </div>
            <p className="text-sm text-gray-500">
              Ready for trading and investments
            </p>
          </div>
        </div>

        {/* Transaction Form */}
        <div className="lg:col-span-2">
          <div className="card p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Add or Withdraw Funds</h2>
            
            {/* Operation Toggle */}
            <div className="flex rounded-lg bg-gray-100 p-1 mb-6">
              <button
                onClick={() => setOperation('add')}
                className={`flex-1 py-3 px-4 rounded-md text-sm font-medium transition-colors flex items-center justify-center space-x-2 ${
                  operation === 'add'
                    ? 'bg-success-600 text-white'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                <Plus className="h-4 w-4" />
                <span>Add Funds</span>
              </button>
              <button
                onClick={() => setOperation('withdraw')}
                className={`flex-1 py-3 px-4 rounded-md text-sm font-medium transition-colors flex items-center justify-center space-x-2 ${
                  operation === 'withdraw'
                    ? 'bg-danger-600 text-white'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                <Minus className="h-4 w-4" />
                <span>Withdraw</span>
              </button>
            </div>

            <form onSubmit={handleTransaction} className="space-y-6">
              {/* Amount Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Amount ($)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <DollarSign className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="input pl-10"
                    placeholder="0.00"
                    required
                  />
                </div>
              </div>

              {/* Quick Amount Buttons */}
              <div>
                <p className="text-sm font-medium text-gray-700 mb-3">Quick amounts:</p>
                <div className="grid grid-cols-4 gap-2">
                  {[100, 500, 1000, 5000].map((quickAmount) => (
                    <button
                      key={quickAmount}
                      type="button"
                      onClick={() => setAmount(quickAmount.toString())}
                      className="btn btn-secondary text-sm py-2"
                    >
                      ${quickAmount}
                    </button>
                  ))}
                </div>
              </div>

              {/* Transaction Summary */}
              {amount && parseFloat(amount) > 0 && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium text-gray-900 mb-2">Transaction Summary</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Operation</span>
                      <span className="font-medium">
                        {operation === 'add' ? 'Add Funds' : 'Withdraw Funds'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Amount</span>
                      <span className="font-medium">${parseFloat(amount).toFixed(2)}</span>
                    </div>
                    <div className="border-t border-gray-200 pt-2">
                      <div className="flex justify-between">
                        <span className="font-medium text-gray-900">New Balance</span>
                        <span className="font-bold">
                          ${operation === 'add' 
                            ? ((funds?.balance || 0) + parseFloat(amount)).toFixed(2)
                            : ((funds?.balance || 0) - parseFloat(amount)).toFixed(2)
                          }
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isProcessing || !amount || parseFloat(amount) <= 0}
                className={`btn w-full flex items-center justify-center space-x-2 ${
                  operation === 'add' ? 'btn-success' : 'btn-danger'
                } ${(isProcessing || !amount || parseFloat(amount) <= 0) ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <CreditCard className="h-4 w-4" />
                <span>
                  {isProcessing 
                    ? 'Processing...' 
                    : `${operation === 'add' ? 'Add' : 'Withdraw'} ${amount || '0.00'}`
                  }
                </span>
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6">
          <div className="flex items-start space-x-3">
            <div className="bg-blue-100 p-2 rounded-full">
              <Plus className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Adding Funds</h3>
              <p className="text-sm text-gray-600">
                Add money to your trading account to start buying stocks. Funds are available immediately for trading.
              </p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-start space-x-3">
            <div className="bg-orange-100 p-2 rounded-full">
              <Minus className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Withdrawing Funds</h3>
              <p className="text-sm text-gray-600">
                Withdraw your available balance back to your bank account. Only uninvested funds can be withdrawn.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Funds;