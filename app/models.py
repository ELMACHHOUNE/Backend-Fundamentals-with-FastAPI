from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current timestamp")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI-generated response")


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100, description="Quiz topic")
    num_questions: int = Field(..., ge=1, le=20, description="Number of questions to generate")

    @field_validator("topic")
    @classmethod
    def topic_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Topic cannot be empty or whitespace only")
        return v.strip()


class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    options: List[str] = Field(..., min_length=2, max_length=6, description="Answer options")
    correct_answer: int = Field(..., ge=0, description="Index of correct answer (0-based)")
    explanation: Optional[str] = Field(None, description="Explanation for the correct answer")


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(..., min_length=1, description="List of quiz questions")


class SummariseRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000, description="Text to summarise")
    max_bullets: int = Field(default=5, ge=1, le=10, description="Maximum number of bullet points")

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class SummariseResponse(BaseModel):
    summary: List[str] = Field(..., min_length=1, description="List of summary bullet points")
    original_length: int = Field(..., description="Length of original text in characters")
    summary_length: int = Field(..., description="Length of summary in characters")