"""Shared Pydantic models for LokVaani services."""

from .base import BaseModel, TimestampedModel
from .session import UserSession, ConversationContext, DeviceInfo, UserPreferences
from .voice import VoiceInteraction, SpeechResult, AudioQualityResult
from .language import LanguageConfig, LanguageDetectionResult, TranslationResult
from .content import ContentProcessingRequest, SimplificationResult, SummaryResult
from .accessibility import AccessibilityConfig

__all__ = [
    "BaseModel",
    "TimestampedModel",
    "UserSession",
    "ConversationContext", 
    "DeviceInfo",
    "UserPreferences",
    "VoiceInteraction",
    "SpeechResult",
    "AudioQualityResult",
    "LanguageConfig",
    "LanguageDetectionResult",
    "TranslationResult",
    "ContentProcessingRequest",
    "SimplificationResult",
    "SummaryResult",
    "AccessibilityConfig",
]