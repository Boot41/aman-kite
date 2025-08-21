import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from app.utils.stock_data import fetch_stock_data, update_stock_prices, search_stocks
from app.models.stock import Stock
from app.config import settings


class TestFetchStockData:
    """Test cases for fetch_stock_data function"""
    
    def test_fetch_stock_data_demo_mode(self):
        """Test fetch_stock_data returns mock data when API key is 'demo'"""
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'demo'):
            result = fetch_stock_data('AAPL')
            
            assert result is not None
            assert result['price'] == 150.25
            assert result['change'] == 2.50
            assert result['change_percent'] == 1.69
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_success(self, mock_get):
        """Test successful API response"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Global Quote": {
                "05. price": "175.50",
                "09. change": "3.25",
                "10. change percent": "1.89%"
            }
        }
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is not None
            assert result['price'] == 175.50
            assert result['change'] == 3.25
            assert result['change_percent'] == 1.89
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_api_limit(self, mock_get):
        """Test API rate limit response"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute"
        }
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_error_message(self, mock_get):
        """Test API error message response"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Error Message": "Invalid API call"
        }
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_information_message(self, mock_get):
        """Test API information message response"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Information": "The **demo** API key is for demo purposes only"
        }
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_no_global_quote(self, mock_get):
        """Test response without Global Quote"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Meta Data": {
                "1. Information": "Daily Prices"
            }
        }
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_request_exception(self, mock_get):
        """Test request exception handling"""
        mock_get.side_effect = Exception("Network error")
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None
    
    @patch('app.utils.stock_data.requests.get')
    def test_fetch_stock_data_json_exception(self, mock_get):
        """Test JSON parsing exception"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        with patch.object(settings, 'ALPHA_VANTAGE_API_KEY', 'test_key'):
            result = fetch_stock_data('AAPL')
            
            assert result is None


class TestUpdateStockPrices:
    """Test cases for update_stock_prices function"""
    
    def test_update_stock_prices_success(self, db_session):
        """Test successful stock price updates"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.00)
        db_session.add_all([stock1, stock2])
        db_session.commit()
        
        with patch('app.utils.stock_data.fetch_stock_data') as mock_fetch:
            mock_fetch.side_effect = [
                {"price": 175.50, "change": 25.50, "change_percent": 17.0},
                {"price": 2850.00, "change": 50.00, "change_percent": 1.79}
            ]
            
            update_stock_prices(db_session)
            
            # Verify prices were updated
            updated_stock1 = db_session.query(Stock).filter_by(ticker_symbol="AAPL").first()
            updated_stock2 = db_session.query(Stock).filter_by(ticker_symbol="GOOGL").first()
            
            assert updated_stock1.current_price == 175.50
            assert updated_stock2.current_price == 2850.00
    
    def test_update_stock_prices_partial_failure(self, db_session):
        """Test update when some stock data fetch fails"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        stock2 = Stock(ticker_symbol="INVALID", company_name="Invalid Stock", current_price=100.00)
        db_session.add_all([stock1, stock2])
        db_session.commit()
        
        with patch('app.utils.stock_data.fetch_stock_data') as mock_fetch:
            mock_fetch.side_effect = [
                {"price": 175.50, "change": 25.50, "change_percent": 17.0},
                None  # Failed fetch for INVALID stock
            ]
            
            update_stock_prices(db_session)
            
            # Verify only successful update was applied
            updated_stock1 = db_session.query(Stock).filter_by(ticker_symbol="AAPL").first()
            updated_stock2 = db_session.query(Stock).filter_by(ticker_symbol="INVALID").first()
            
            assert updated_stock1.current_price == 175.50
            assert updated_stock2.current_price == 100.00  # Unchanged


class TestSearchStocks:
    """Test cases for search_stocks function"""
    
    def test_search_stocks_by_ticker(self, db_session):
        """Test searching stocks by ticker symbol"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.00)
        stock3 = Stock(ticker_symbol="MSFT", company_name="Microsoft Corporation", current_price=300.00)
        db_session.add_all([stock1, stock2, stock3])
        db_session.commit()
        
        results = search_stocks(db_session, "AAP")
        
        assert len(results) == 1
        assert results[0].ticker_symbol == "AAPL"
    
    def test_search_stocks_by_company_name(self, db_session):
        """Test searching stocks by company name"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.00)
        stock3 = Stock(ticker_symbol="MSFT", company_name="Microsoft Corporation", current_price=300.00)
        db_session.add_all([stock1, stock2, stock3])
        db_session.commit()
        
        results = search_stocks(db_session, "Apple")
        
        assert len(results) == 1
        assert results[0].company_name == "Apple Inc."
    
    def test_search_stocks_case_insensitive(self, db_session):
        """Test case insensitive search"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        db_session.add(stock1)
        db_session.commit()
        
        results = search_stocks(db_session, "apple")
        
        assert len(results) == 1
        assert results[0].company_name == "Apple Inc."
    
    def test_search_stocks_multiple_matches(self, db_session):
        """Test search returning multiple matches"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.00)
        stock3 = Stock(ticker_symbol="AMZN", company_name="Amazon.com Inc.", current_price=3200.00)
        db_session.add_all([stock1, stock2, stock3])
        db_session.commit()
        
        results = search_stocks(db_session, "A")
        
        assert len(results) == 3  # All contain 'A'
    
    def test_search_stocks_no_matches(self, db_session):
        """Test search with no matches"""
        # Create test stocks
        stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
        db_session.add(stock1)
        db_session.commit()
        
        results = search_stocks(db_session, "NONEXISTENT")
        
        assert len(results) == 0
