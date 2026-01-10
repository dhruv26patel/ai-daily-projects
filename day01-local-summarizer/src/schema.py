from pydantic import BaseModel, Field
from typing import List, Literal


class SummaryResult(BaseModel):
    """
    This defines the exact output format we expect from the AI.

    Think: "contract" for the AI output.
    If the AI returns something weird, Pydantic will complain,
    and we can handle it safely.
    """  
    summary: str = Field(..., description="A brief summary of the input text.")
    top_issues: List[str] = Field(..., description="A list of the top issues identified in the text.")
    action_items: List[str] = Field(..., description="A list of recommended action items.")
    severity: Literal["low", "medium", "high"] = Field(..., description="The severity level of the issues.")

