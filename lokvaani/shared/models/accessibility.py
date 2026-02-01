"""Accessibility-related models for LokVaani."""

from pydantic import Field
from typing import Optional, List, Dict
from enum import Enum

from .base import BaseModel


class ContrastLevel(str, Enum):
    """Contrast level options."""
    NORMAL = "normal"
    HIGH = "high"
    MAXIMUM = "maximum"


class TextSize(str, Enum):
    """Text size options."""
    SMALL = "small"
    NORMAL = "normal"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


class NavigationMode(str, Enum):
    """Navigation mode preferences."""
    MOUSE = "mouse"
    KEYBOARD = "keyboard"
    TOUCH = "touch"
    VOICE = "voice"
    MIXED = "mixed"


class AccessibilityConfig(BaseModel):
    """Accessibility configuration for users."""
    
    # Screen reader support
    screen_reader_support: bool = Field(False, description="Whether screen reader support is enabled")
    screen_reader_type: Optional[str] = Field(None, description="Type of screen reader being used")
    
    # Visual accessibility
    high_contrast_mode: bool = Field(False, description="Whether high contrast mode is enabled")
    contrast_level: ContrastLevel = Field(ContrastLevel.NORMAL, description="Contrast level setting")
    text_size_multiplier: float = Field(1.0, ge=0.8, le=3.0, description="Text size multiplier")
    text_size: TextSize = Field(TextSize.NORMAL, description="Text size preference")
    
    # Audio accessibility
    audio_speed_multiplier: float = Field(1.0, ge=0.25, le=4.0, description="Audio playback speed multiplier")
    audio_descriptions: bool = Field(False, description="Whether audio descriptions are enabled")
    captions_enabled: bool = Field(False, description="Whether captions are enabled")
    
    # Navigation accessibility
    keyboard_navigation_enabled: bool = Field(False, description="Whether keyboard navigation is enabled")
    preferred_navigation_mode: NavigationMode = Field(NavigationMode.MIXED, description="Preferred navigation method")
    focus_indicators_enhanced: bool = Field(False, description="Whether enhanced focus indicators are enabled")
    
    # Alternative content
    alternative_text_enabled: bool = Field(True, description="Whether alternative text is enabled")
    simplified_interface: bool = Field(False, description="Whether simplified interface is enabled")
    reduced_motion: bool = Field(False, description="Whether reduced motion is preferred")
    
    # Color and visual indicators
    color_blind_support: bool = Field(False, description="Whether color blind support is enabled")
    color_blind_type: Optional[str] = Field(None, description="Type of color blindness")
    use_patterns_for_color: bool = Field(False, description="Whether to use patterns instead of color")
    
    def get_text_size_pixels(self, base_size: int = 16) -> int:
        """Calculate text size in pixels based on multiplier."""
        return int(base_size * self.text_size_multiplier)
    
    def requires_alternative_indicators(self) -> bool:
        """Check if alternative indicators are needed for color information."""
        return self.color_blind_support or self.use_patterns_for_color
    
    def get_audio_speed(self) -> float:
        """Get the audio playback speed setting."""
        return self.audio_speed_multiplier


class AccessibilityFeature(BaseModel):
    """Description of an accessibility feature."""
    
    feature_id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Human-readable feature name")
    description: str = Field(..., description="Description of what the feature does")
    category: str = Field(..., description="Category of accessibility feature")
    is_available: bool = Field(True, description="Whether the feature is currently available")
    requires_configuration: bool = Field(False, description="Whether the feature requires user configuration")
    
    # WCAG compliance information
    wcag_level: Optional[str] = Field(None, description="WCAG compliance level (A, AA, AAA)")
    wcag_criteria: List[str] = Field(default_factory=list, description="WCAG success criteria addressed")


class AccessibilityReport(BaseModel):
    """Report on accessibility compliance and features."""
    
    overall_score: float = Field(..., ge=0, le=100, description="Overall accessibility score")
    wcag_compliance_level: str = Field(..., description="Highest WCAG level achieved")
    supported_features: List[AccessibilityFeature] = Field(..., description="List of supported accessibility features")
    missing_features: List[str] = Field(default_factory=list, description="List of missing accessibility features")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")
    
    # Compliance details
    level_a_compliance: bool = Field(..., description="Whether WCAG Level A is achieved")
    level_aa_compliance: bool = Field(..., description="Whether WCAG Level AA is achieved")
    level_aaa_compliance: bool = Field(..., description="Whether WCAG Level AAA is achieved")
    
    def get_features_by_category(self, category: str) -> List[AccessibilityFeature]:
        """Get accessibility features by category."""
        return [feature for feature in self.supported_features if feature.category == category]
    
    def is_feature_supported(self, feature_id: str) -> bool:
        """Check if a specific accessibility feature is supported."""
        return any(feature.feature_id == feature_id for feature in self.supported_features)


class AccessibilityRequest(BaseModel):
    """Request to update accessibility settings."""
    
    session_id: str = Field(..., description="Session identifier")
    config: AccessibilityConfig = Field(..., description="New accessibility configuration")
    apply_immediately: bool = Field(True, description="Whether to apply changes immediately")


class AccessibilityResponse(BaseModel):
    """Response for accessibility configuration operations."""
    
    success: bool = Field(..., description="Whether the configuration was applied successfully")
    current_config: AccessibilityConfig = Field(..., description="Current accessibility configuration")
    applied_changes: List[str] = Field(default_factory=list, description="List of changes that were applied")
    error_message: Optional[str] = Field(None, description="Error message if operation failed")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations based on the configuration")