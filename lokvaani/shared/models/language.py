"""Language processing models for LokVaani."""

from pydantic import Field
from typing import Optional, List, Dict
from enum import Enum

from .base import BaseModel, ProcessingMetrics


class LanguageCandidate(BaseModel):
    """A candidate language with confidence score."""
    
    language_code: str = Field(..., description="ISO 639-1 language code")
    language_name: str = Field(..., description="Human-readable language name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for this language")


class LanguageDetectionResult(BaseModel):
    """Result of language detection."""
    
    primary_language: str = Field(..., description="Most likely language code")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in primary language detection")
    alternative_languages: List[LanguageCandidate] = Field(default_factory=list, description="Alternative language candidates")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")
    
    def is_confident(self, threshold: float = 0.8) -> bool:
        """Check if detection confidence meets threshold."""
        return self.confidence >= threshold


class TranslationResult(BaseModel):
    """Result of text translation."""
    
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Detected source language")
    target_language: str = Field(..., description="Target language for translation")
    confidence: float = Field(..., ge=0, le=1, description="Translation confidence score")
    alternative_translations: List[str] = Field(default_factory=list, description="Alternative translation options")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")


class VoiceOption(BaseModel):
    """Available voice option for a language."""
    
    voice_name: str = Field(..., description="Unique voice identifier")
    display_name: str = Field(..., description="Human-readable voice name")
    gender: str = Field(..., description="Voice gender (male, female, neutral)")
    age_group: str = Field(..., description="Voice age group (child, adult, elderly)")
    accent: Optional[str] = Field(None, description="Voice accent or regional variant")
    is_premium: bool = Field(False, description="Whether this is a premium voice")
    sample_rate: int = Field(22050, description="Default sample rate for this voice")


class LanguageConfig(BaseModel):
    """Configuration for a supported language."""
    
    language_code: str = Field(..., description="ISO 639-1 language code")
    display_name: str = Field(..., description="Human-readable language name")
    native_name: str = Field(..., description="Language name in its native script")
    is_supported: bool = Field(True, description="Whether this language is currently supported")
    stt_available: bool = Field(True, description="Whether speech-to-text is available")
    tts_available: bool = Field(True, description="Whether text-to-speech is available")
    translation_available: bool = Field(True, description="Whether translation is available")
    voice_options: List[VoiceOption] = Field(default_factory=list, description="Available voice options")
    
    # Language-specific settings
    rtl_script: bool = Field(False, description="Whether language uses right-to-left script")
    requires_special_handling: bool = Field(False, description="Whether language requires special processing")
    fallback_language: Optional[str] = Field(None, description="Fallback language if processing fails")
    
    def get_default_voice(self) -> Optional[VoiceOption]:
        """Get the default voice option for this language."""
        if not self.voice_options:
            return None
        
        # Prefer non-premium voices as default
        non_premium = [v for v in self.voice_options if not v.is_premium]
        if non_premium:
            return non_premium[0]
        
        return self.voice_options[0]
    
    def get_voice_by_name(self, voice_name: str) -> Optional[VoiceOption]:
        """Get a specific voice option by name."""
        for voice in self.voice_options:
            if voice.voice_name == voice_name:
                return voice
        return None


class LanguagePreferenceRequest(BaseModel):
    """Request to set language preference."""
    
    session_id: str = Field(..., description="Session identifier")
    language_code: str = Field(..., description="Preferred language code")
    explicit_request: bool = Field(True, description="Whether this was an explicit user request")


class LanguagePreferenceResponse(BaseModel):
    """Response for language preference operations."""
    
    success: bool = Field(..., description="Whether the preference was set successfully")
    current_language: str = Field(..., description="Current language setting")
    available_languages: List[str] = Field(..., description="List of available language codes")
    error_message: Optional[str] = Field(None, description="Error message if operation failed")


class MultilingualText(BaseModel):
    """Text content in multiple languages."""
    
    texts: Dict[str, str] = Field(..., description="Text content keyed by language code")
    primary_language: str = Field(..., description="Primary language of the content")
    
    def get_text(self, language_code: str, fallback: bool = True) -> Optional[str]:
        """Get text in specified language with optional fallback."""
        if language_code in self.texts:
            return self.texts[language_code]
        
        if fallback and self.primary_language in self.texts:
            return self.texts[self.primary_language]
        
        # Return any available text as last resort
        if fallback and self.texts:
            return next(iter(self.texts.values()))
        
        return None
    
    def add_translation(self, language_code: str, text: str) -> None:
        """Add a translation for the specified language."""
        self.texts[language_code] = text