from pydantic import BaseModel
from typing import Optional


class ClassificationRequest(BaseModel):
    statement: str
    available_disciplines: list[str]
    available_subjects: dict[str, list[str]]


class ClassificationResponse(BaseModel):
    discipline: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    confidence: str = "low"
    ai_available: bool = True
    error_message: Optional[str] = None