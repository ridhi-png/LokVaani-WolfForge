"""SQLAlchemy database models for LokVaani."""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Float, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


class DatabaseModel(Base):
    """Base model for all database tables."""
    
    __abstract__ = True
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class UserSessionDB(DatabaseModel):
    """Database model for user sessions."""
    
    __tablename__ = "user_sessions"
    
    session_id = Column(String, unique=True, nullable=False, index=True)
    device_info = Column(JSON, nullable=False)
    language_preference = Column(String, default="en", nullable=False)
    last_activity = Column(DateTime, default=func.now(), nullable=False)
    conversation_context = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<UserSession(session_id='{self.session_id}', language='{self.language_preference}')>"


class VoiceInteractionDB(DatabaseModel):
    """Database model for voice interactions."""
    
    __tablename__ = "voice_interactions"
    
    interaction_id = Column(String, unique=True, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    input_type = Column(String, nullable=False)
    processed_text = Column(Text, nullable=False)
    detected_language = Column(String, nullable=False)
    response_text = Column(Text, nullable=False)
    voice_config = Column(JSON, nullable=True)
    processing_metrics = Column(JSON, nullable=False)
    audio_quality = Column(JSON, nullable=True)
    speech_result = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<VoiceInteraction(interaction_id='{self.interaction_id}', session_id='{self.session_id}')>"


class ContentProcessingDB(DatabaseModel):
    """Database model for content processing requests."""
    
    __tablename__ = "content_processing"
    
    request_id = Column(String, unique=True, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    original_content = Column(Text, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    simplification_level = Column(String, nullable=False)
    requested_format = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    max_length = Column(Integer, nullable=True)
    preserve_technical_terms = Column(Boolean, default=False)
    source_info = Column(JSON, nullable=True)
    processing_result = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<ContentProcessing(request_id='{self.request_id}', session_id='{self.session_id}')>"


class LanguageConfigDB(DatabaseModel):
    """Database model for language configurations."""
    
    __tablename__ = "language_configs"
    
    language_code = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    native_name = Column(String, nullable=False)
    is_supported = Column(Boolean, default=True, nullable=False)
    stt_available = Column(Boolean, default=True, nullable=False)
    tts_available = Column(Boolean, default=True, nullable=False)
    translation_available = Column(Boolean, default=True, nullable=False)
    voice_options = Column(JSON, nullable=False, default=list)
    rtl_script = Column(Boolean, default=False, nullable=False)
    requires_special_handling = Column(Boolean, default=False, nullable=False)
    fallback_language = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<LanguageConfig(language_code='{self.language_code}', display_name='{self.display_name}')>"


class AccessibilityConfigDB(DatabaseModel):
    """Database model for accessibility configurations."""
    
    __tablename__ = "accessibility_configs"
    
    session_id = Column(String, nullable=False, index=True)
    screen_reader_support = Column(Boolean, default=False, nullable=False)
    screen_reader_type = Column(String, nullable=True)
    high_contrast_mode = Column(Boolean, default=False, nullable=False)
    contrast_level = Column(String, default="normal", nullable=False)
    text_size_multiplier = Column(Float, default=1.0, nullable=False)
    text_size = Column(String, default="normal", nullable=False)
    audio_speed_multiplier = Column(Float, default=1.0, nullable=False)
    audio_descriptions = Column(Boolean, default=False, nullable=False)
    captions_enabled = Column(Boolean, default=False, nullable=False)
    keyboard_navigation_enabled = Column(Boolean, default=False, nullable=False)
    preferred_navigation_mode = Column(String, default="mixed", nullable=False)
    focus_indicators_enhanced = Column(Boolean, default=False, nullable=False)
    alternative_text_enabled = Column(Boolean, default=True, nullable=False)
    simplified_interface = Column(Boolean, default=False, nullable=False)
    reduced_motion = Column(Boolean, default=False, nullable=False)
    color_blind_support = Column(Boolean, default=False, nullable=False)
    color_blind_type = Column(String, nullable=True)
    use_patterns_for_color = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<AccessibilityConfig(session_id='{self.session_id}')>"