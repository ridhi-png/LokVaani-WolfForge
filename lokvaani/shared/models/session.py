"""Session-related models for LokVaani."""

from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from .base import BaseModel, TimestampedModel, IdentifiedModel


class InputType(str, Enum):
    """Types of user input."""
    VOICE = "voice"
    TEXT = "text"


class DeviceInfo(BaseModel):
    """Information about the user's device."""
    
    device_type: str = Field(..., description="Type of device (mobile, desktop, tablet)")
    user_agent: Optional[str] = Field(None, description="Browser user agent string")
    screen_width: Optional[int] = Field(None, ge=1, description="Screen width in pixels")
    screen_height: Optional[int] = Field(None, ge=1, description="Screen height in pixels")
    supports_audio: bool = Field(True, description="Whether device supports audio")
    supports_microphone: bool = Field(True, description="Whether device has microphone access")


class UserPreferences(BaseModel):
    """User preferences for the session."""
    
    preferred_language: str = Field("en", description="User's preferred language code")
    input_type: InputType = Field(InputType.VOICE, description="Preferred input method")
    audio_speed_multiplier: float = Field(1.0, ge=0.5, le=2.0, description="Audio playback speed multiplier")
    text_size_multiplier: float = Field(1.0, ge=0.8, le=2.0, description="Text size multiplier")
    high_contrast_mode: bool = Field(False, description="Whether high contrast mode is enabled")
    screen_reader_support: bool = Field(False, description="Whether screen reader support is needed")


class QueryHistory(BaseModel):
    """A single query in the conversation history."""
    
    query_id: str = Field(..., description="Unique identifier for the query")
    user_input: str = Field(..., description="The user's input text")
    input_type: InputType = Field(..., description="Type of input (voice or text)")
    detected_language: str = Field(..., description="Detected language of the input")
    response_text: str = Field(..., description="The system's response text")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: float = Field(ge=0, description="Time taken to process the query")


class ContextualData(BaseModel):
    """Contextual information for the conversation."""
    
    current_topic: Optional[str] = Field(None, description="Current conversation topic")
    mentioned_entities: List[str] = Field(default_factory=list, description="Entities mentioned in conversation")
    user_intent: Optional[str] = Field(None, description="Detected user intent")
    conversation_stage: str = Field("initial", description="Stage of the conversation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional contextual metadata")


class ConversationContext(BaseModel):
    """Context for a conversation session."""
    
    previous_queries: List[QueryHistory] = Field(default_factory=list, description="History of queries in this session")
    user_preferences: UserPreferences = Field(default_factory=UserPreferences)
    current_topic: Optional[str] = Field(None, description="Current conversation topic")
    contextual_information: ContextualData = Field(default_factory=ContextualData)
    
    def add_query(self, query: QueryHistory) -> None:
        """Add a query to the conversation history."""
        self.previous_queries.append(query)
        
        # Keep only the most recent queries to prevent unbounded growth
        max_history = 50  # Configurable limit
        if len(self.previous_queries) > max_history:
            self.previous_queries = self.previous_queries[-max_history:]
    
    def get_recent_context(self, num_queries: int = 5) -> List[QueryHistory]:
        """Get the most recent queries for context."""
        return self.previous_queries[-num_queries:] if self.previous_queries else []


class UserSession(TimestampedModel, IdentifiedModel):
    """A user session with conversation context."""
    
    session_id: str = Field(..., description="Unique session identifier")
    device_info: DeviceInfo = Field(..., description="Information about the user's device")
    language_preference: str = Field("en", description="User's preferred language")
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    conversation_context: ConversationContext = Field(default_factory=ConversationContext)
    is_active: bool = Field(True, description="Whether the session is currently active")
    
    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_activity = datetime.utcnow()
        self.update_timestamp()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if the session has expired."""
        from datetime import timedelta
        timeout_delta = timedelta(minutes=timeout_minutes)
        return datetime.utcnow() - self.last_activity > timeout_delta
    
    def terminate(self) -> None:
        """Terminate the session."""
        self.is_active = False
        self.update_timestamp()