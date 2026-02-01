"""Configuration management for LokVaani services."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database Configuration
    database_url: str = "postgresql://lokvaani:lokvaani@localhost:5432/lokvaani"
    test_database_url: str = "postgresql://lokvaani:lokvaani@localhost:5432/lokvaani_test"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    test_redis_url: str = "redis://localhost:6379/1"
    
    # Google Cloud API Configuration
    google_cloud_api_key: Optional[str] = None
    google_application_credentials: Optional[str] = None
    
    # OpenAI API Configuration
    openai_api_key: Optional[str] = None
    
    # Service Configuration
    api_gateway_host: str = "0.0.0.0"
    api_gateway_port: int = 8000
    voice_service_host: str = "0.0.0.0"
    voice_service_port: int = 8001
    language_service_host: str = "0.0.0.0"
    language_service_port: int = 8002
    content_service_host: str = "0.0.0.0"
    content_service_port: int = 8003
    session_service_host: str = "0.0.0.0"
    session_service_port: int = 8004
    
    # Security Configuration
    secret_key: str = "your_secret_key_here_change_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Session Configuration
    session_timeout_minutes: int = 30
    max_conversation_context_size: int = 1000
    
    # Performance Configuration
    max_concurrent_requests: int = 100
    request_timeout_seconds: int = 30
    audio_processing_timeout_seconds: int = 10
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Development Configuration
    debug: bool = False
    reload: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_database_url(test: bool = False) -> str:
    """Get the appropriate database URL based on environment."""
    if test or os.getenv("TESTING"):
        return settings.test_database_url
    return settings.database_url


def get_redis_url(test: bool = False) -> str:
    """Get the appropriate Redis URL based on environment."""
    if test or os.getenv("TESTING"):
        return settings.test_redis_url
    return settings.redis_url