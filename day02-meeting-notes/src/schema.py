from pydantic import BaseModel, Field
from typing import List, Literal


class ActionItem(BaseModel):
    task: str = Field(..., description="Action to do")
    owner: str = Field(..., description="Person responsible or 'unknown'")
    priority: Literal["low", "medium", "high"] = Field(..., description="Priority level")
    due_date: str = Field(..., description="YYYY-MM-DD or 'unknown'")


class SummaryResult(BaseModel):
    summary: str = Field(..., description="Short summary under 3 lines")
    action_items: List[ActionItem] = Field(..., description="3 to 6 action items")
