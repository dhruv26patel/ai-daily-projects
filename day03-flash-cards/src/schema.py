from pydantic import BaseModel, Field
from typing import List, Literal


class FlashCard(BaseModel):
    question: str = Field(..., description="Flash card question text")
    answer: str = Field(..., description="Flash card answer text")
    difficulty: Literal["easy", "medium", "hard"] = Field(..., description="Difficulty level")


class TopicSummaryResult(BaseModel):
    topics: List[str] = Field(..., description="List of topics covered")
    flash_cards: List[FlashCard] = Field(..., description="List of flash cards")
