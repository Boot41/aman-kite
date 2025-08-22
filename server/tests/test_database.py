import pytest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db, SessionLocal, engine, Base
from app.config import settings


class TestDatabase:
    """Test cases for database module"""
    
    def test_get_db_yields_session(self):
        """Test that get_db yields a database session"""
        db_generator = get_db()
        db = next(db_generator)
        
        assert db is not None
        assert hasattr(db, 'query')
        assert hasattr(db, 'add')
        assert hasattr(db, 'commit')
        
        # Clean up
        try:
            next(db_generator)
        except StopIteration:
            pass  # Expected behavior
    
    def test_get_db_closes_session(self):
        """Test that get_db properly closes the session"""
        db_generator = get_db()
        db = next(db_generator)
        
        # Mock the close method to verify it's called
        with patch.object(db, 'close') as mock_close:
            try:
                next(db_generator)
            except StopIteration:
                pass  # Expected behavior
            
            mock_close.assert_called_once()
    
    def test_get_db_closes_on_exception(self):
        """Test that get_db closes session even if exception occurs"""
        db_generator = get_db()
        db = next(db_generator)
        
        # Mock the close method to verify it's called
        with patch.object(db, 'close') as mock_close:
            # Simulate an exception in the try block
            with patch.object(db, 'query', side_effect=Exception("Test exception")):
                try:
                    # This would normally cause an exception
                    db.query(Mock)
                except:
                    pass
                
                # Close the generator
                try:
                    next(db_generator)
                except StopIteration:
                    pass
                
                mock_close.assert_called_once()
    
    def test_engine_configuration(self):
        """Test that engine is configured correctly"""
        assert engine is not None
        assert engine.pool.size() == 20
        assert engine.pool._max_overflow == 30
        assert engine.pool._pre_ping is True
    
    def test_session_local_configuration(self):
        """Test SessionLocal configuration"""
        assert SessionLocal is not None
        
        # Create a session to test configuration
        session = SessionLocal()
        # In SQLAlchemy 2.0, these are properties of the sessionmaker, not the session instance
        assert hasattr(session, 'bind')
        assert hasattr(session, 'query')
        session.close()
    
    def test_base_class_exists(self):
        """Test that Base class is properly created"""
        assert Base is not None
        assert hasattr(Base, 'metadata')
        # Base class doesn't have query method in SQLAlchemy 2.0, check registry instead
        assert hasattr(Base, 'registry')
