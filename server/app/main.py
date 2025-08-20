from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine, get_db, Base
from app import models, schemas
from api import auth, stocks, holdings, transactions, funds, watchlist

# Initialize FastAPI app
app = FastAPI(
    title="Stock Trading API",
    description="A Zerodha-like stock trading platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(holdings.router, prefix="/api/portfolio/holdings", tags=["Holdings"])
app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(funds.router, prefix="/api/portfolio/funds", tags=["Funds"])
app.include_router(watchlist.router, prefix="/api/watchlist", tags=["Watchlist"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stock Trading API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)