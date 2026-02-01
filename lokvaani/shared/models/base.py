"""Base models for LokVaani services."""

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
import uuid


class BaseModel(PydanticBaseModel):
    """Base model with common configuration."""
    
    model_config = ConfigDict(
        # Enable validation on assignment
        validate_assignment=True,
        # Use enum values instead of names
        use_enum_values=True,
        # Allow population by field name or alias
        populate_by_name=True,
        # Validate default values
        validate_default=True,
        # Extra fields are forbidden
        extra="forbid",
    )


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class IdentifiedModel(BaseModel):
    """Base model with UUID identifier."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class ProcessingMetrics(BaseModel):
    """Metrics for processing operations."""
    
    processing_time_ms: float = Field(ge=0, description="Processing time in milliseconds")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Confidence score between 0 and 1")
    error_count: int = Field(0, ge=0, description="Number of errors encountered")
    retry_count: int = Field(0, ge=0, description="Number of retries attempted")