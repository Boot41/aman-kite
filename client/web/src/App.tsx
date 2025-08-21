import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/layout/Layout';

// Auth Components
import Login from './components/auth/Login';
import Register from './components/auth/Register';

// Pages
import Dashboard from './pages/Dashboard';
import Holdings from './pages/Holdings';
import StockDetails from './pages/StockDetails';
import Transactions from './pages/Transactions';
import Funds from './pages/Funds';
import Watchlist from './pages/Watchlist';
import AIInsights from './pages/AIInsights';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="holdings" element={<Holdings />} />
            <Route path="stocks/:ticker" element={<StockDetails />} />
            <Route path="transactions" element={<Transactions />} />
            <Route path="funds" element={<Funds />} />
            <Route path="watchlist" element={<Watchlist />} />
            <Route path="ai-insights" element={<AIInsights />} />
          </Route>
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
