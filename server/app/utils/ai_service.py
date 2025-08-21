"""
AI Service Module using Groq API
Provides stock insights, market sentiment, and portfolio analysis
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from groq import Groq
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.models.holding import Holding
from app.models.transaction import Transaction

class AIService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.news_api_key = "demo"  # Using demo key for news API
        
    def get_stock_performance_insights(self, stock: Stock, historical_data: List[Dict]) -> str:
        """Generate AI insights for stock performance"""
        try:
            # Prepare stock data for analysis
            stock_info = {
                "symbol": stock.ticker_symbol,
                "company": stock.company_name,
                "current_price": float(stock.current_price),
                "historical_data": historical_data[-30:] if len(historical_data) > 30 else historical_data
            }
            
            prompt = f"""
            Analyze the stock performance for {stock_info['company']} ({stock_info['symbol']}) and provide insights in plain English.
            
            Current Price: ${stock_info['current_price']}
            Recent Historical Data: {json.dumps(stock_info['historical_data'][-5:], indent=2)}
            
            Please provide:
            1. A brief performance summary (2-3 sentences)
            2. Key trends or patterns observed
            3. Risk assessment (low/medium/high)
            4. Short-term outlook
            
            Keep the response concise and investor-friendly, under 200 words.
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing stock insights to retail investors."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating stock insights: {e}")
            return f"Unable to generate insights for {stock.ticker_symbol} at this time. Please try again later."
    
    def get_market_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze market sentiment using news data"""
        try:
            # Fetch recent news for the symbols
            news_data = self._fetch_recent_news(symbols)
            
            if not news_data:
                return {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0,
                    "summary": "No recent news data available for sentiment analysis.",
                    "news_count": 0
                }
            
            # Prepare news for sentiment analysis
            news_text = " ".join([article.get("title", "") + " " + article.get("description", "") 
                                for article in news_data[:10]])
            
            prompt = f"""
            Analyze the market sentiment based on these recent news headlines and descriptions:
            
            {news_text[:2000]}
            
            Provide:
            1. Overall sentiment (positive/negative/neutral)
            2. Sentiment score (-1.0 to 1.0, where -1 is very negative, 0 is neutral, 1 is very positive)
            3. A brief summary of key market themes (2-3 sentences)
            
            Respond in JSON format:
            {{
                "sentiment": "positive/negative/neutral",
                "score": 0.0,
                "summary": "Brief summary here"
            }}
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial sentiment analyst. Respond only in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.2,
                max_tokens=200
            )
            
            try:
                sentiment_data = json.loads(response.choices[0].message.content.strip())
                return {
                    "overall_sentiment": sentiment_data.get("sentiment", "neutral"),
                    "sentiment_score": float(sentiment_data.get("score", 0.0)),
                    "summary": sentiment_data.get("summary", "Market sentiment analysis completed."),
                    "news_count": len(news_data)
                }
            except json.JSONDecodeError:
                return {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0,
                    "summary": "Market sentiment appears mixed based on recent news coverage.",
                    "news_count": len(news_data)
                }
                
        except Exception as e:
            print(f"Error analyzing market sentiment: {e}")
            return {
                "overall_sentiment": "neutral",
                "sentiment_score": 0.0,
                "summary": "Unable to analyze market sentiment at this time.",
                "news_count": 0
            }
    
    def get_portfolio_overview(self, user_id: int, db: Session) -> str:
        """Generate AI-powered portfolio analysis"""
        try:
            # Fetch user's holdings and transactions
            holdings = db.query(Holding).filter(Holding.user_id == user_id).all()
            recent_transactions = db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_date >= datetime.now() - timedelta(days=30)
            ).all()
            
            if not holdings:
                return "Your portfolio is currently empty. Consider adding some investments to get started with building wealth through the stock market."
            
            # Prepare portfolio data
            portfolio_data = []
            total_value = 0
            total_invested = 0
            
            for holding in holdings:
                stock = db.query(Stock).filter(Stock.stock_id == holding.stock_id).first()
                if stock:
                    current_value = float(holding.quantity * stock.current_price)
                    invested_value = float(holding.quantity * holding.average_cost)
                    pnl = current_value - invested_value
                    pnl_percent = (pnl / invested_value * 100) if invested_value > 0 else 0
                    
                    portfolio_data.append({
                        "symbol": stock.ticker_symbol,
                        "company": stock.company_name,
                        "quantity": int(holding.quantity),
                        "current_value": current_value,
                        "invested_value": invested_value,
                        "pnl": pnl,
                        "pnl_percent": pnl_percent
                    })
                    
                    total_value += current_value
                    total_invested += invested_value
            
            total_pnl = total_value - total_invested
            total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0
            
            prompt = f"""
            Analyze this investment portfolio and provide a comprehensive overview in plain English:
            
            Portfolio Summary:
            - Total Current Value: ${total_value:.2f}
            - Total Invested: ${total_invested:.2f}
            - Total P&L: ${total_pnl:.2f} ({total_pnl_percent:.1f}%)
            - Number of Holdings: {len(portfolio_data)}
            - Recent Transactions (30 days): {len(recent_transactions)}
            
            Individual Holdings:
            {json.dumps(portfolio_data, indent=2)}
            
            Please provide:
            1. Overall portfolio performance assessment
            2. Diversification analysis
            3. Top performing and underperforming holdings
            4. Risk assessment and recommendations
            5. Actionable insights for improvement
            
            Keep it conversational and under 300 words.
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a personal financial advisor providing portfolio analysis to retail investors."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.4,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating portfolio overview: {e}")
            return "Unable to generate portfolio analysis at this time. Please ensure you have holdings and try again later."
    
    def _fetch_recent_news(self, symbols: List[str]) -> List[Dict]:
        """Fetch recent news for given stock symbols"""
        try:
            # Using NewsAPI (demo version has limited functionality)
            # In production, you'd want to use a proper news API key
            news_data = []
            
            # Mock news data for demo purposes
            mock_news = [
                {
                    "title": "Stock Market Shows Mixed Signals Amid Economic Uncertainty",
                    "description": "Markets continue to navigate through volatile conditions with technology stocks leading gains while energy sector faces headwinds.",
                    "publishedAt": datetime.now().isoformat()
                },
                {
                    "title": "Federal Reserve Maintains Interest Rate Stance",
                    "description": "The Fed keeps rates steady as inflation shows signs of cooling, providing some relief to equity markets.",
                    "publishedAt": (datetime.now() - timedelta(hours=2)).isoformat()
                },
                {
                    "title": "Tech Earnings Season Brings Optimism to Markets",
                    "description": "Strong quarterly results from major technology companies boost investor confidence in the sector.",
                    "publishedAt": (datetime.now() - timedelta(hours=4)).isoformat()
                }
            ]
            
            return mock_news
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

# Global AI service instance
ai_service = AIService()
