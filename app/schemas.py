from pydantic import BaseModel

class TicketDecisionRequest(BaseModel):
    ticketText: str
    confidence: float
    processInstanceId: str


class TicketDecisionResponse(BaseModel):
    processInstanceId: str
    priority: str
    category: str
    urgency: str
    sentiment: str
    expectedResolutionHours: int
    recommendedAction: str
    requiresHumanReview: bool
