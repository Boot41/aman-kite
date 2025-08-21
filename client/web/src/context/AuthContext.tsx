import React, { useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User } from '../types';
import { authAPI } from '../services/api';
import { AuthContext } from './AuthContext.hooks';

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        } catch (error: unknown) {
          localStorage.removeItem('token');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      console.log('AuthContext: Starting login for username:', username);
      const response = await authAPI.login({ username, password });
      console.log('AuthContext: Login response:', response);
      localStorage.setItem('token', response.access_token);
      const userData = await authAPI.getCurrentUser();
      console.log('AuthContext: User data:', userData);
      setUser(userData);
    } catch (error: unknown) {
      console.error('AuthContext: Login error:', error);
      throw error;
    }
  };

  const register = async (username: string, email: string, password: string) => {
    try {
      console.log('AuthContext: Starting registration for:', { username, email });
      const registerResponse = await authAPI.register({ username, email, password });
      console.log('AuthContext: Registration successful:', registerResponse);
      
      // Auto-login after registration
      console.log('AuthContext: Starting auto-login with username:', username);
      await login(username, password);
      console.log('AuthContext: Auto-login successful');
    } catch (error: unknown) {
      console.error('AuthContext: Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Re-export useAuth hook
export { useAuth } from './AuthContext.hooks';