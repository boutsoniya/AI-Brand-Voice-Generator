from typing import List
from pydantic import BaseModel, Field

class ToneProfile(BaseModel):
    formality: int = Field(ge=0, le=10)
    warmth: int = Field(ge=0, le=10)
    confidence: int = Field(ge=0, le=10)
    playfulness: int = Field(ge=0, le=10)
    technicality: int = Field(ge=0, le=10)

class SentenceStyle(BaseModel):
    average_length: str
    rhythm: str
    complexity: str
    punctuation_style: str

class VoiceProfile(BaseModel):
    personality: List[str]
    tone: ToneProfile
    sentence_style: SentenceStyle
    preferred_vocabulary: List[str]
    preferred_patterns: List[str]
    avoid: List[str]
    audience_relationship: str
    summary: str
