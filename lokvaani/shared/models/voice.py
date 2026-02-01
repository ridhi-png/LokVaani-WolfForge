"""Voice processing models for LokVaani."""

from pydantic import Field
from datetime import datetime
from typing import Optional, List, Union
from enum import Enum

from .base import BaseModel, TimestampedModel, IdentifiedModel, ProcessingMetrics
from .session import InputType


class AudioFormat(str, Enum):
    """Supported audio formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"


class AudioQuality(str, Enum):
    """Audio quality levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class VoiceConfig(BaseModel):
    """Configuration for voice synthesis."""
    
    language_code: str = Field(..., description="Language code for voice synthesis")
    voice_name: Optional[str] = Field(None, description="Specific voice name to use")
    speaking_rate: float = Field(1.0, ge=0.25, le=4.0, description="Speaking rate multiplier")
    pitch: float = Field(0.0, ge=-20.0, le=20.0, description="Voice pitch adjustment in semitones")
    volume_gain_db: float = Field(0.0, ge=-96.0, le=16.0, description="Volume gain in decibels")
    audio_format: AudioFormat = Field(AudioFormat.MP3, description="Output audio format")
    sample_rate: int = Field(22050, description="Audio sample rate in Hz")


class SpeechResult(BaseModel):
    """Result of speech-to-text conversion."""
    
    text: str = Field(..., description="Transcribed text from speech")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of transcription")
    detected_language: str = Field(..., description="Detected language code")
    alternative_transcriptions: List[str] = Field(default_factory=list, description="Alternative transcription options")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")


class AudioQualityResult(BaseModel):
    """Result of audio quality assessment."""
    
    is_acceptable: bool = Field(..., description="Whether audio quality is acceptable for processing")
    quality_score: float = Field(..., ge=0, le=1, description="Audio quality score")
    noise_level: float = Field(..., ge=0, le=1, description="Background noise level")
    signal_to_noise_ratio: Optional[float] = Field(None, description="Signal-to-noise ratio in dB")
    issues: List[str] = Field(default_factory=list, description="Identified audio quality issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")


class VoiceInteraction(TimestampedModel, IdentifiedModel):
    """A complete voice interaction record."""
    
    interaction_id: str = Field(..., description="Unique interaction identifier")
    session_id: str = Field(..., description="Associated session identifier")
    input_type: InputType = Field(..., description="Type of input (voice or text)")
    input_data: Union[str, bytes] = Field(..., description="Raw input data (text or audio bytes)")
    processed_text: str = Field(..., description="Processed text from input")
    detected_language: str = Field(..., description="Detected input language")
    response_text: str = Field(..., description="Generated response text")
    response_audio: Optional[bytes] = Field(None, description="Generated response audio data")
    voice_config: Optional[VoiceConfig] = Field(None, description="Voice configuration used")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")
    
    # Audio-specific fields
    audio_quality: Optional[AudioQualityResult] = Field(None, description="Audio quality assessment")
    speech_result: Optional[SpeechResult] = Field(None, description="Speech recognition result")
    
    def is_voice_input(self) -> bool:
        """Check if this interaction used voice input."""
        return self.input_type == InputType.VOICE
    
    def has_audio_response(self) -> bool:
        """Check if this interaction has an audio response."""
        return self.response_audio is not None


class AudioControlRequest(BaseModel):
    """Request for audio playback control."""
    
    interaction_id: str = Field(..., description="Interaction ID for the audio")
    action: str = Field(..., description="Control action (play, pause, stop, replay, speed)")
    speed_multiplier: Optional[float] = Field(None, ge=0.25, le=4.0, description="Speed multiplier for playback")
    position_seconds: Optional[float] = Field(None, ge=0, description="Playback position in seconds")


class AudioControlResponse(BaseModel):
    """Response for audio control operations."""
    
    success: bool = Field(..., description="Whether the control operation succeeded")
    current_position: Optional[float] = Field(None, description="Current playback position in seconds")
    duration: Optional[float] = Field(None, description="Total audio duration in seconds")
    is_playing: bool = Field(False, description="Whether audio is currently playing")
    error_message: Optional[str] = Field(None, description="Error message if operation failed")