# 🪁 Kite - AI-Powered Stock Trading Platform

A comprehensive stock trading web application similar to Zerodha, built with modern technologies and enhanced with AI-powered insights.

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
- **Real-time Price Updates** - Integration with Alpha Vantage API
- **Responsive Design** - Beautiful UI that works on all devices
- **Comprehensive Dashboard** - Overview of portfolio, P&L, and market data
- **Search & Discovery** - Find and analyze stocks easily

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
- **Alpha Vantage API** for real-time stock data

### Database Schema
```sql
Users → Holdings → Stocks
  ↓       ↓         ↓
Funds  Transactions Watchlist
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and **pnpm**
- **Python** 3.10+
- **PostgreSQL** 12+
- **Groq API Key** (for AI features)
- **Alpha Vantage API Key** (for stock data)

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
# Edit .env with your database and API credentials

# Run database migrations
alembic upgrade head

# Seed database with sample stocks
python scripts/seed_database.py

# Start backend server
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd client/web

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

### 4. Access Application
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Environment Variables

### Backend (`.env`)
```env
DATABASE_URL=postgresql://username:password@localhost/kite_db
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
```

## 📁 Project Structure

```
aman-kite/
├── client/web/                 # React frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Application pages
│   │   ├── services/          # API integration
│   │   └── types/             # TypeScript definitions
│   ├── public/                # Static assets
│   └── package.json
├── server/                    # FastAPI backend
│   ├── api/                   # API route handlers
│   ├── app/                   # Core application logic
│   │   ├── models/            # Database models
│   │   └── schemas/           # Pydantic schemas
│   ├── scripts/               # Utility scripts
│   ├── alembic/              # Database migrations
│   └── requirements.txt
└── project/                   # Documentation
    ├── specs.md
    ├── architecture.md
    └── apis.md
```

## 🧪 Testing

### Backend Tests
```bash
cd server
pytest                         # Run all tests
pytest -v                      # Verbose output
pytest --cov                   # With coverage report
```

### Frontend Tests
```bash
cd client/web
pnpm test                      # Run tests
pnpm test:coverage            # With coverage
```

## 🚀 Deployment

### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Deploy with your preferred service (Railway, Heroku, etc.)

### Frontend Deployment
1. Build the application: `pnpm build`
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

Powered by **Groq's LLaMA 3 8B model** for:
- Natural language stock analysis
- Market sentiment interpretation
- Portfolio performance insights
- Risk assessment and recommendations

## 📊 Supported Stock Data

- **20+ Pre-loaded Stocks** - Major US stocks (AAPL, GOOGL, MSFT, etc.)
- **Real-time Prices** - Alpha Vantage API integration
- **Historical Data** - Price history and trends
- **Market Data** - Volume, market cap, and key metrics

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

- **Alpha Vantage** for stock market data
- **Groq** for AI-powered insights
- **React Team** for the amazing frontend framework
- **FastAPI** for the high-performance backend framework

## 📞 Support

For support, email support@kite-trading.com or create an issue on GitHub.

---

**Built with ❤️ by [Your Name]**

*Making stock trading intelligent and accessible for everyone.*
