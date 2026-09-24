from pydantic import BaseModel, Field
from typing import List

class ConsistencyResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    tone_score: int = Field(ge=0, le=100)
    vocabulary_score: int = Field(ge=0, le=100)
    structure_score: int = Field(ge=0, le=100)
    audience_fit: int = Field(ge=0, le=100)
    issues: List[str]
    suggestions: List[str]
