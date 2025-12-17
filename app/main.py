from fastapi import FastAPI
from typing import Optional
from app.ai import ask
from app.schemas import TicketDecisionRequest, TicketDecisionResponse
from app.decision_service import decide

app = FastAPI(
    title="AI Ticket Decision Service (Groq)",
    description="Groq-powered AI decision engine for Flowable",
    version="1.0"
)

# -----------------------------
# Helper: generate confidence
# -----------------------------
def generate_conf_from_ticket(ticket: str) -> float:
    response = ask(f"Score clarity 0.0–1.0:\n{ticket}")
    try:
        return max(0.0, min(float(response), 1.0))
    except Exception:
        return 0.5


# -----------------------------
# Endpoint: /prioritize
# Accepts JSON with 'ticketText'
# -----------------------------
@app.post("/prioritize", response_model=TicketDecisionResponse)
def prioritize_ticket(request: TicketDecisionRequest):
    # Use 'ticket' from request; can map from 'ticketText' if needed
    ticket_text = getattr(request, "ticket", None)  # fallback in case alias is used
    if not ticket_text:
        raise ValueError("ticketText is required")

    confidence = request.confidence or generate_conf_from_ticket(ticket_text)

    decision = decide(ticket=ticket_text, confidence=confidence)

    return TicketDecisionResponse(
        processInstanceId=request.processInstanceId,
        **decision
    )


# -----------------------------
# Endpoint: /predict
# Accepts JSON with 'ticket'
# -----------------------------
@app.post("/predict", response_model=TicketDecisionResponse)
def predict(request: TicketDecisionRequest):
    ticket_text = request.ticket
    if not ticket_text:
        raise ValueError("ticket is required")

    confidence = request.confidence or generate_conf_from_ticket(ticket_text)

    decision = decide(ticket=ticket_text, confidence=confidence)

    return TicketDecisionResponse(
        processInstanceId=request.processInstanceId,
        **decision
    )
