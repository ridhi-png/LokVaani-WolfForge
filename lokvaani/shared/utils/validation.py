"""Validation utilities for LokVaani services."""

import re
from typing import List, Optional
from pydantic import ValidationError as PydanticValidationError

from .exceptions import ValidationError


# Language code patterns
LANGUAGE_CODE_PATTERN = re.compile(r'^[a-z]{2}(-[A-Z]{2})?$')
SESSION_ID_PATTERN = re.compile(r'^[a-zA-Z0-9\-_]{8,64}$')

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {'wav', 'mp3', 'flac', 'ogg', 'webm', 'm4a'}

# Supported language codes (ISO 639-1 with optional country codes)
SUPPORTED_LANGUAGES = {
    'en', 'en-US', 'en-GB', 'en-AU', 'en-CA',
    'hi', 'hi-IN',
    'es', 'es-ES', 'es-MX', 'es-AR',
    'fr', 'fr-FR', 'fr-CA',
    'de', 'de-DE',
    'it', 'it-IT',
    'pt', 'pt-BR', 'pt-PT',
    'ru', 'ru-RU',
    'ja', 'ja-JP',
    'ko', 'ko-KR',
    'zh', 'zh-CN', 'zh-TW',
    'ar', 'ar-SA',
    'bn', 'bn-BD', 'bn-IN',
    'ur', 'ur-PK',
    'ta', 'ta-IN',
    'te', 'te-IN',
    'ml', 'ml-IN',
    'kn', 'kn-IN',
    'gu', 'gu-IN',
    'pa', 'pa-IN',
    'mr', 'mr-IN',
    'or', 'or-IN',
    'as', 'as-IN',
}


def validate_language_code(language_code: str, strict: bool = True) -> str:
    """
    Validate a language code.
    
    Args:
        language_code: The language code to validate
        strict: If True, only allow supported languages
        
    Returns:
        The validated language code
        
    Raises:
        ValidationError: If the language code is invalid
    """
    if not language_code:
        raise ValidationError("Language code cannot be empty")
    
    language_code = language_code.strip().lower()
    
    # Check format
    if not LANGUAGE_CODE_PATTERN.match(language_code):
        raise ValidationError(f"Invalid language code format: {language_code}")
    
    # Check if supported (if strict mode)
    if strict and language_code not in SUPPORTED_LANGUAGES:
        raise ValidationError(f"Unsupported language code: {language_code}")
    
    return language_code


def validate_session_id(session_id: str) -> str:
    """
    Validate a session ID.
    
    Args:
        session_id: The session ID to validate
        
    Returns:
        The validated session ID
        
    Raises:
        ValidationError: If the session ID is invalid
    """
    if not session_id:
        raise ValidationError("Session ID cannot be empty")
    
    session_id = session_id.strip()
    
    if not SESSION_ID_PATTERN.match(session_id):
        raise ValidationError(f"Invalid session ID format: {session_id}")
    
    return session_id


def validate_audio_format(audio_format: str) -> str:
    """
    Validate an audio format.
    
    Args:
        audio_format: The audio format to validate
        
    Returns:
        The validated audio format
        
    Raises:
        ValidationError: If the audio format is invalid
    """
    if not audio_format:
        raise ValidationError("Audio format cannot be empty")
    
    audio_format = audio_format.strip().lower()
    
    if audio_format not in SUPPORTED_AUDIO_FORMATS:
        raise ValidationError(f"Unsupported audio format: {audio_format}")
    
    return audio_format


def validate_text_length(text: str, max_length: int = 10000, min_length: int = 1) -> str:
    """
    Validate text length.
    
    Args:
        text: The text to validate
        max_length: Maximum allowed length
        min_length: Minimum required length
        
    Returns:
        The validated text
        
    Raises:
        ValidationError: If the text length is invalid
    """
    if not text:
        raise ValidationError("Text cannot be empty")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValidationError(f"Text too short: minimum {min_length} characters required")
    
    if len(text) > max_length:
        raise ValidationError(f"Text too long: maximum {max_length} characters allowed")
    
    return text


def validate_confidence_score(score: float) -> float:
    """
    Validate a confidence score.
    
    Args:
        score: The confidence score to validate
        
    Returns:
        The validated confidence score
        
    Raises:
        ValidationError: If the confidence score is invalid
    """
    if not isinstance(score, (int, float)):
        raise ValidationError("Confidence score must be a number")
    
    if not 0.0 <= score <= 1.0:
        raise ValidationError("Confidence score must be between 0.0 and 1.0")
    
    return float(score)


def validate_audio_speed_multiplier(multiplier: float) -> float:
    """
    Validate an audio speed multiplier.
    
    Args:
        multiplier: The speed multiplier to validate
        
    Returns:
        The validated speed multiplier
        
    Raises:
        ValidationError: If the speed multiplier is invalid
    """
    if not isinstance(multiplier, (int, float)):
        raise ValidationError("Speed multiplier must be a number")
    
    if not 0.25 <= multiplier <= 4.0:
        raise ValidationError("Speed multiplier must be between 0.25 and 4.0")
    
    return float(multiplier)


def validate_pydantic_model(model_class, data: dict) -> object:
    """
    Validate data against a Pydantic model.
    
    Args:
        model_class: The Pydantic model class
        data: The data to validate
        
    Returns:
        The validated model instance
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        return model_class(**data)
    except PydanticValidationError as e:
        error_messages = []
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error['loc'])
            message = error['msg']
            error_messages.append(f"{field}: {message}")
        
        raise ValidationError(f"Validation failed: {'; '.join(error_messages)}")


def get_supported_languages() -> List[str]:
    """Get list of supported language codes."""
    return sorted(list(SUPPORTED_LANGUAGES))


def get_supported_audio_formats() -> List[str]:
    """Get list of supported audio formats."""
    return sorted(list(SUPPORTED_AUDIO_FORMATS))