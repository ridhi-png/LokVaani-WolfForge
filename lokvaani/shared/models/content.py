"""Content processing models for LokVaani."""

from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from .base import BaseModel, TimestampedModel, IdentifiedModel, ProcessingMetrics


class AudienceLevel(str, Enum):
    """Target audience complexity levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResponseFormat(str, Enum):
    """Supported response formats."""
    TEXT = "text"
    AUDIO = "audio"
    BOTH = "both"


class ContentType(str, Enum):
    """Types of content being processed."""
    INFORMATIONAL = "informational"
    INSTRUCTIONAL = "instructional"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    NEWS = "news"
    EDUCATIONAL = "educational"


class TermExplanation(BaseModel):
    """Explanation of a technical term."""
    
    term: str = Field(..., description="The technical term")
    definition: str = Field(..., description="Plain language definition")
    context: Optional[str] = Field(None, description="Context where the term appears")
    examples: List[str] = Field(default_factory=list, description="Usage examples")
    related_terms: List[str] = Field(default_factory=list, description="Related technical terms")


class ContentSource(BaseModel):
    """Information about content source."""
    
    source_id: str = Field(..., description="Unique source identifier")
    name: str = Field(..., description="Source name")
    url: Optional[str] = Field(None, description="Source URL")
    authority_score: float = Field(..., ge=0, le=1, description="Authority/reliability score")
    last_updated: Optional[datetime] = Field(None, description="When content was last updated")
    content_type: ContentType = Field(..., description="Type of content from this source")
    is_official: bool = Field(False, description="Whether this is an official/authoritative source")


class ContentProcessingRequest(TimestampedModel, IdentifiedModel):
    """Request for content processing and simplification."""
    
    request_id: str = Field(..., description="Unique request identifier")
    session_id: str = Field(..., description="Associated session identifier")
    original_content: str = Field(..., description="Original content to process")
    source_language: str = Field(..., description="Language of the original content")
    target_language: str = Field(..., description="Target language for response")
    simplification_level: AudienceLevel = Field(AudienceLevel.BEGINNER, description="Target audience level")
    requested_format: ResponseFormat = Field(ResponseFormat.BOTH, description="Requested response format")
    content_type: ContentType = Field(ContentType.INFORMATIONAL, description="Type of content being processed")
    max_length: Optional[int] = Field(None, ge=1, description="Maximum length for response")
    preserve_technical_terms: bool = Field(False, description="Whether to preserve technical terminology")
    source_info: Optional[ContentSource] = Field(None, description="Information about content source")


class SimplificationResult(BaseModel):
    """Result of content simplification."""
    
    simplified_text: str = Field(..., description="Simplified version of the content")
    complexity_reduction: float = Field(..., ge=0, le=1, description="Measure of complexity reduction achieved")
    preserved_key_points: List[str] = Field(..., description="Key information points preserved")
    technical_terms_explained: List[TermExplanation] = Field(default_factory=list, description="Technical terms with explanations")
    readability_score: Optional[float] = Field(None, ge=0, le=100, description="Readability score of simplified text")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")
    
    def get_explanation_for_term(self, term: str) -> Optional[TermExplanation]:
        """Get explanation for a specific technical term."""
        for explanation in self.technical_terms_explained:
            if explanation.term.lower() == term.lower():
                return explanation
        return None


class SummaryResult(BaseModel):
    """Result of content summarization."""
    
    summary_text: str = Field(..., description="Summarized content")
    original_length: int = Field(..., ge=0, description="Length of original content in characters")
    summary_length: int = Field(..., ge=0, description="Length of summary in characters")
    compression_ratio: float = Field(..., ge=0, le=1, description="Ratio of summary to original length")
    key_points: List[str] = Field(..., description="Key points extracted from content")
    topics_covered: List[str] = Field(default_factory=list, description="Main topics covered in summary")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")


class ExplanationResult(BaseModel):
    """Result of technical term explanation."""
    
    explanations: List[TermExplanation] = Field(..., description="List of term explanations")
    terms_found: int = Field(..., ge=0, description="Number of technical terms identified")
    terms_explained: int = Field(..., ge=0, description="Number of terms successfully explained")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")


class AccuracyResult(BaseModel):
    """Result of factual accuracy validation."""
    
    is_accurate: bool = Field(..., description="Whether simplified content maintains accuracy")
    accuracy_score: float = Field(..., ge=0, le=1, description="Factual accuracy score")
    discrepancies: List[str] = Field(default_factory=list, description="Identified factual discrepancies")
    missing_information: List[str] = Field(default_factory=list, description="Important information that was lost")
    added_information: List[str] = Field(default_factory=list, description="Information added during simplification")
    processing_metrics: ProcessingMetrics = Field(..., description="Processing performance metrics")


class ContentResponse(BaseModel):
    """Complete response for content processing."""
    
    request_id: str = Field(..., description="Original request identifier")
    processed_content: str = Field(..., description="Final processed content")
    content_language: str = Field(..., description="Language of the processed content")
    simplification_result: Optional[SimplificationResult] = Field(None, description="Simplification details")
    summary_result: Optional[SummaryResult] = Field(None, description="Summary details if requested")
    explanation_result: Optional[ExplanationResult] = Field(None, description="Term explanations if requested")
    accuracy_result: Optional[AccuracyResult] = Field(None, description="Accuracy validation results")
    source_attribution: Optional[ContentSource] = Field(None, description="Source attribution information")
    processing_time_ms: float = Field(..., ge=0, description="Total processing time")
    
    def has_simplification(self) -> bool:
        """Check if response includes simplification."""
        return self.simplification_result is not None
    
    def has_explanations(self) -> bool:
        """Check if response includes term explanations."""
        return (self.explanation_result is not None and 
                len(self.explanation_result.explanations) > 0)