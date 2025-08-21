# 🪁 Kite - AI-Powered Stock Trading Platform

A comprehensive stock trading web application similar to Zerodha, built with modern technologies and enhanced with AI-powered insights.

## 🎬 Demo Video

[![Kite Trading Platform Demo](https://img.shields.io/badge/Watch%20Demo-Loom-FF5722?style=for-the-badge&logo=loom)](https://www.loom.com/share/1f8ccbbc46294065885c301415c3839f?sid=d4e41f8d-711f-42ef-b098-8f34306a4682)

*Click above to watch a comprehensive demo of all features including AI insights, trading functionality, and portfolio management.*

![React](https://img.shields.io/badge/React-19.1.1-61DAFB?style=flat&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=flat&logo=postgresql)
![TypeScript](https://img.shields.io/badge/TypeScript-5.8.3-3178C6?style=flat&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)

## ✨ Features

### 🔐 Core Trading Features
- **User Authentication** - Secure registration, login, and JWT-based sessions
- **Real-time Portfolio Management** - Track holdings, P&L, and portfolio value
- **Stock Trading** - Buy/sell stocks with real-time price updates
- **Transaction History** - Complete audit trail of all trades
- **Funds Management** - Add/withdraw funds with balance tracking
- **Watchlist** - Monitor favorite stocks and market movements

### 🤖 AI-Powered Insights
- **Stock Performance Analysis** - AI-generated insights on stock trends and patterns
- **Market Sentiment Analysis** - Real-time sentiment analysis from news data
- **Portfolio Overview** - Intelligent analysis of portfolio performance and recommendations
- **Risk Assessment** - AI-powered risk evaluation for individual stocks and portfolio

### 📊 Advanced Features
- **Real-time Price Updates** - Integration with Finnhub API for live market data
- **Responsive Design** - Beautiful UI that works on all devices
- **Comprehensive Dashboard** - Overview of portfolio, P&L, and market data
- **Search & Discovery** - Find and analyze stocks with real-time quotes
- **Market News Integration** - Latest financial news and market updates
- **Technical Indicators** - Real-time technical analysis data

## 🏗️ Architecture

### Frontend (`/client/web/`)
- **React 19** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for modern, responsive styling
- **React Router** for navigation
- **Axios** for API communication
- **Lucide React** for beautiful icons

### Backend (`/server/`)
- **FastAPI** with Python 3.10+
- **SQLAlchemy** ORM with PostgreSQL
- **Alembic** for database migrations
- **JWT Authentication** with secure token handling
- **Groq AI Integration** for intelligent insights
- **Finnhub API** for real-time stock data and market information

### Database Schema
```sql
Users → Holdings → Stocks
  ↓       ↓         ↓
Funds  Transactions Watchlist
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and **npm**
- **Python** 3.10+
- **PostgreSQL** 12+
- **Groq API Key** (for AI features)
- **Finnhub API Key** (for real-time stock data)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/aman-kite.git
cd aman-kite
```

### 2. Backend Setup
```bash
cd server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database and API credentials:
# DATABASE_URL=postgresql://username:password@localhost/stockapp
# SECRET_KEY=your-super-secret-jwt-key
# GROQ_API_KEY=your-groq-api-key
# FINNHUB_API_KEY=your-finnhub-api-key

# Run database migrations
alembic upgrade head

# Seed database with sample stocks
python scripts/seed_database.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd client/web

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:5173 (or http://localhost:5174 if port 5173 is in use)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Environment Variables

### Backend (`.env`)
```env
# Database
DATABASE_URL=postgresql://aman:yourpassword@localhost/stockapp

# JWT
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
FINNHUB_API_KEY=your-finnhub-api-key
GROQ_API_KEY=your-groq-api-key

# Settings
DEBUG=True
```

## 📁 Project Structure

```
aman-kite/
├── client/web/                 # React frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Application pages (Dashboard, AIInsights, etc.)
│   │   ├── services/          # API integration (api.ts)
│   │   └── types/             # TypeScript definitions
│   ├── public/                # Static assets
│   ├── package.json           # npm dependencies
│   └── package-lock.json      # npm lockfile
├── server/                    # FastAPI backend
│   ├── api/                   # API route handlers (auth.py, ai.py, etc.)
│   ├── app/                   # Core application logic
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── utils/             # Utility functions (auth, ai_service)
│   │   ├── database.py        # Database configuration
│   │   └── config.py          # App configuration
│   ├── scripts/               # Utility scripts (seed_database.py)
│   ├── alembic/              # Database migrations
│   ├── tests/                # Test files
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── test.db              # SQLite test database
├── project/                   # Documentation
│   ├── specs.md
│   ├── architecture.md
│   └── apis.md
└── README.md                  # This file
```

## 🧪 Testing

### Backend Tests
```bash
cd server
# Activate virtual environment first
source .venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov

# Run specific test files
pytest test_ai_endpoints.py
pytest test_portfolio.py
```

### Frontend Tests
```bash
cd client/web
# Run tests (when implemented)
npm test

# Run with coverage (when implemented)
npm run test:coverage
```

## 🚀 Deployment

### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Deploy with your preferred service (Railway, Heroku, etc.)

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy the `dist/` folder to your hosting service
3. Configure environment variables for production API URL

## 🤝 API Documentation

The backend provides a comprehensive REST API with the following endpoints:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Trading
- `GET /api/stocks` - List available stocks
- `POST /api/trade` - Execute buy/sell orders
- `GET /api/holdings` - Get user holdings
- `GET /api/transactions` - Transaction history

### Portfolio
- `GET /api/portfolio/current-value` - Real-time portfolio value
- `POST /api/portfolio/refresh-prices` - Update stock prices

### AI Features
- `GET /api/ai/stock-insights/{ticker}` - AI stock analysis
- `GET /api/ai/market-sentiment` - Market sentiment analysis
- `GET /api/ai/portfolio-overview` - Portfolio AI insights

Full API documentation available at `/docs` when running the server.

## 🎨 UI/UX Features

- **Modern Design** - Clean, professional interface inspired by leading trading platforms
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Real-time Updates** - Live data updates without page refresh
- **Interactive Charts** - Visual representation of portfolio performance
- **Dark/Light Mode** - Comfortable viewing in any environment
- **Accessibility** - WCAG compliant design for all users

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt for secure password storage
- **CORS Protection** - Configured for secure cross-origin requests
- **Input Validation** - Comprehensive validation on all inputs
- **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection

## 🤖 AI Integration

Powered by **Groq's LLaMA 3 8B model** (llama3-8b-8192) for:
- **Stock Performance Analysis** - AI analyzes stock data and provides plain English summaries with risk assessment
- **Market Sentiment Analysis** - Fetches news and runs sentiment analysis (positive/negative/neutral)
- **Portfolio Overview** - Analyzes user holdings and generates natural language summaries with recommendations
- **Risk Assessment** - AI-powered risk evaluation for individual stocks and overall portfolio

## 📊 Supported Stock Data

- **20 Pre-loaded Stocks** - Major US stocks including:
  - AAPL (Apple Inc.), GOOGL (Alphabet Inc.), MSFT (Microsoft Corporation)
  - AMZN (Amazon.com Inc.), TSLA (Tesla Inc.), NVDA (NVIDIA Corporation)
  - JPM (JPMorgan Chase & Co.), V (Visa Inc.), WMT (Walmart Inc.)
  - DIS (The Walt Disney Company), NFLX (Netflix Inc.), and more
- **Real-time Prices** - Finnhub API integration for live market data and quotes
- **Historical Data** - Price history and trends analysis
- **Market Data** - Volume, market cap, and key financial metrics

## 🛠️ Development

### Code Style
- **Frontend**: ESLint + Prettier for TypeScript/React
- **Backend**: Black + isort for Python formatting
- **Commits**: Conventional commit messages

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Finnhub** for comprehensive stock market data and real-time quotes
- **Groq** for AI-powered insights
- **React Team** for the amazing frontend framework
- **FastAPI** for the high-performance backend framework


