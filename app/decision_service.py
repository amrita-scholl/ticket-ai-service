import json
from app.groq_client import analyze_ticket

def decide(ticket_text: str, confidence: float):
    ai_output = analyze_ticket(ticket_text)
    ai_result = json.loads(ai_output)

    # 1️⃣ Confidence governance
    requires_human_review = confidence < 0.6
    if requires_human_review:
        ai_result["recommendedAction"] = "MANUAL_REVIEW"

    # 2️⃣ SLA hard limits
    if ai_result["priority"] == "CRITICAL":
        ai_result["expectedResolutionHours"] = min(
            ai_result["expectedResolutionHours"], 2
        )

    # 3️⃣ Sentiment-based escalation
    if ai_result["sentiment"] == "ANGRY" and ai_result["priority"] != "CRITICAL":
        ai_result["priority"] = "HIGH"

    return {
        "priority": ai_result["priority"],
        "category": ai_result["category"],
        "urgency": ai_result["urgency"],
        "sentiment": ai_result["sentiment"],
        "expectedResolutionHours": ai_result["expectedResolutionHours"],
        "recommendedAction": ai_result["recommendedAction"],
        "requiresHumanReview": requires_human_review
    }
