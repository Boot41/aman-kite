import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app


class TestMainApp:
    """Test cases for main FastAPI application"""
    
    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = self.client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Stock Trading API"}
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "API is running successfully"
    
    def test_app_metadata(self):
        """Test FastAPI app metadata"""
        assert app.title == "Stock Trading API"
        assert app.description == "A Zerodha-like stock trading platform API"
        assert app.version == "1.0.0"
    
    def test_cors_middleware_configured(self):
        """Test CORS middleware is properly configured"""
        # Test preflight request
        response = self.client.options(
            "/api/stocks/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Should not return 405 Method Not Allowed for OPTIONS
        assert response.status_code != 405
    
    def test_cors_headers_present(self):
        """Test CORS headers are present in responses"""
        response = self.client.get(
            "/",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
    
    def test_invalid_endpoint_404(self):
        """Test invalid endpoint returns 404"""
        response = self.client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
    
    def test_api_endpoints_registered(self):
        """Test that all API router endpoints are registered"""
        # Test some key endpoints exist (they should return proper responses, not 404)
        endpoints_to_test = [
            "/api/auth/register",
            "/api/stocks/",
            "/api/portfolio/holdings/",
            "/api/watchlist/",
            "/api/ai/market-sentiment"
        ]
        
        for endpoint in endpoints_to_test:
            response = self.client.get(endpoint)
            # Should not be 404 (endpoint exists), might be 401/422/etc based on auth/validation
            assert response.status_code != 404, f"Endpoint {endpoint} not found"
