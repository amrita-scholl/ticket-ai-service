from pydantic import BaseModel
from typing import Optional


class TicketDecisionRequest(BaseModel):
    ticket: str
    confidence: Optional[float] = None
    processInstanceId: str


class TicketDecisionResponse(BaseModel):
    processInstanceId: str
    priority: str
    confidence: float  
    category: str
    urgency: str
    sentiment: str
    expectedResolutionHours: int
    recommendedAction: str
    requiresHumanReview: bool
