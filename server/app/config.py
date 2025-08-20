import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://aman:yourpassword@localhost/stockapp")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # API Keys (for stock data - you might want to integrate with a real API later)
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    
    # App Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()