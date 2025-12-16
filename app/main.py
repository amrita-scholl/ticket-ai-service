from fastapi import FastAPI
from app.schemas import (
    TicketDecisionRequest,
    TicketDecisionResponse
)
from app.decision_service import decide

app = FastAPI(
    title="AI Ticket Decision Service (Groq)",
    description="Groq-powered AI decision engine for Flowable",
    version="1.0"
)

@app.post("/prioritize", response_model=TicketDecisionResponse)
def prioritize_ticket(request: TicketDecisionRequest):

    decision = decide(
        ticket_text=request.ticketText,
        confidence=request.confidence
    )

    return TicketDecisionResponse(
        processInstanceId=request.processInstanceId,
        **decision
    )
