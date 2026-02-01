"""Database connection management for LokVaani."""

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import redis
from typing import Generator, Optional
import logging

from ..config import get_database_url, get_redis_url

logger = logging.getLogger(__name__)

# Global engine and session factory instances
_engine: Optional[Engine] = None
_session_factory: Optional[sessionmaker] = None
_redis_client: Optional[redis.Redis] = None


def get_database_engine(test: bool = False) -> Engine:
    """Get or create the database engine."""
    global _engine
    
    if _engine is None:
        database_url = get_database_url(test=test)
        
        # Configure engine based on database type
        if database_url.startswith("sqlite"):
            # SQLite configuration for testing
            _engine = create_engine(
                database_url,
                poolclass=StaticPool,
                connect_args={"check_same_thread": False},
                echo=False,  # Set to True for SQL debugging
            )
        else:
            # PostgreSQL configuration for production
            _engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                echo=False,  # Set to True for SQL debugging
            )
        
        logger.info(f"Database engine created for: {database_url}")
    
    return _engine


def get_session_factory(test: bool = False) -> sessionmaker:
    """Get or create the session factory."""
    global _session_factory
    
    if _session_factory is None:
        engine = get_database_engine(test=test)
        _session_factory = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )
        logger.info("Database session factory created")
    
    return _session_factory


def get_database_session(test: bool = False) -> Generator[Session, None, None]:
    """Get a database session with automatic cleanup."""
    session_factory = get_session_factory(test=test)
    session = session_factory()
    
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_redis_client(test: bool = False) -> redis.Redis:
    """Get or create the Redis client."""
    global _redis_client
    
    if _redis_client is None:
        redis_url = get_redis_url(test=test)
        
        _redis_client = redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30,
        )
        
        # Test the connection
        try:
            _redis_client.ping()
            logger.info(f"Redis client connected to: {redis_url}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    return _redis_client


def close_database_connections():
    """Close all database connections."""
    global _engine, _session_factory, _redis_client
    
    if _engine:
        _engine.dispose()
        _engine = None
        logger.info("Database engine disposed")
    
    if _session_factory:
        _session_factory = None
        logger.info("Session factory cleared")
    
    if _redis_client:
        _redis_client.close()
        _redis_client = None
        logger.info("Redis client closed")


def reset_connections():
    """Reset all connections (useful for testing)."""
    close_database_connections()
    logger.info("All database connections reset")