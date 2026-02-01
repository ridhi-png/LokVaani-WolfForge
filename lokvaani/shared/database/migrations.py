"""Database migration utilities for LokVaani."""

from sqlalchemy import text
from sqlalchemy.orm import Session
import logging

from .connection import get_database_engine, get_database_session
from .models import Base

logger = logging.getLogger(__name__)


def create_tables(test: bool = False):
    """Create all database tables."""
    engine = get_database_engine(test=test)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def drop_tables(test: bool = False):
    """Drop all database tables."""
    engine = get_database_engine(test=test)
    Base.metadata.drop_all(bind=engine)
    logger.info("Database tables dropped successfully")


def run_migrations(test: bool = False):
    """Run database migrations."""
    logger.info("Starting database migrations...")
    
    try:
        # Create tables
        create_tables(test=test)
        
        # Seed initial data
        seed_initial_data(test=test)
        
        logger.info("Database migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        raise


def seed_initial_data(test: bool = False):
    """Seed initial data into the database."""
    logger.info("Seeding initial data...")
    
    with get_database_session(test=test) as session:
        # Seed language configurations
        seed_language_configs(session)
        
        session.commit()
        logger.info("Initial data seeded successfully")


def seed_language_configs(session: Session):
    """Seed initial language configurations."""
    from .models import LanguageConfigDB
    
    # Check if language configs already exist
    existing_count = session.query(LanguageConfigDB).count()
    if existing_count > 0:
        logger.info("Language configurations already exist, skipping seed")
        return
    
    # Default language configurations
    languages = [
        {
            "language_code": "en",
            "display_name": "English",
            "native_name": "English",
            "is_supported": True,
            "stt_available": True,
            "tts_available": True,
            "translation_available": True,
            "voice_options": [
                {
                    "voice_name": "en-US-Standard-A",
                    "display_name": "English (US) - Female",
                    "gender": "female",
                    "age_group": "adult",
                    "accent": "US",
                    "is_premium": False,
                    "sample_rate": 22050
                },
                {
                    "voice_name": "en-US-Standard-B",
                    "display_name": "English (US) - Male",
                    "gender": "male",
                    "age_group": "adult",
                    "accent": "US",
                    "is_premium": False,
                    "sample_rate": 22050
                }
            ],
            "rtl_script": False,
            "requires_special_handling": False,
            "fallback_language": None
        },
        {
            "language_code": "hi",
            "display_name": "Hindi",
            "native_name": "हिन्दी",
            "is_supported": True,
            "stt_available": True,
            "tts_available": True,
            "translation_available": True,
            "voice_options": [
                {
                    "voice_name": "hi-IN-Standard-A",
                    "display_name": "Hindi (India) - Female",
                    "gender": "female",
                    "age_group": "adult",
                    "accent": "IN",
                    "is_premium": False,
                    "sample_rate": 22050
                }
            ],
            "rtl_script": False,
            "requires_special_handling": False,
            "fallback_language": "en"
        },
        {
            "language_code": "es",
            "display_name": "Spanish",
            "native_name": "Español",
            "is_supported": True,
            "stt_available": True,
            "tts_available": True,
            "translation_available": True,
            "voice_options": [
                {
                    "voice_name": "es-ES-Standard-A",
                    "display_name": "Spanish (Spain) - Female",
                    "gender": "female",
                    "age_group": "adult",
                    "accent": "ES",
                    "is_premium": False,
                    "sample_rate": 22050
                }
            ],
            "rtl_script": False,
            "requires_special_handling": False,
            "fallback_language": "en"
        }
    ]
    
    for lang_data in languages:
        lang_config = LanguageConfigDB(**lang_data)
        session.add(lang_config)
    
    logger.info(f"Seeded {len(languages)} language configurations")


def reset_database(test: bool = False):
    """Reset the database by dropping and recreating all tables."""
    logger.info("Resetting database...")
    
    try:
        drop_tables(test=test)
        create_tables(test=test)
        seed_initial_data(test=test)
        
        logger.info("Database reset completed successfully")
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise