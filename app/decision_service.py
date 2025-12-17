import json
from typing import Optional
from app.groq_client import analyze_ticket


def decide(ticket_text: str, confidence: Optional[float] = None):
    """
    Decide ticket handling using AI output.
    If confidence is not provided, it is computed from the LLM.
    """

    # 1️⃣ Call LLM (single source of truth for AI fields)
    ai_output = analyze_ticket(ticket_text)
    ai_result = json.loads(ai_output)

    # 2️⃣ Confidence handling
    if confidence is None:
        confidence = ai_result.get("confidence", 0.0)

    # Safety clamp
    confidence = max(0.0, min(confidence, 1.0))

    # 3️⃣ Confidence governance
    requires_human_review = confidence < 0.6
    if requires_human_review:
        ai_result["recommendedAction"] = "MANUAL_REVIEW"

    # 4️⃣ SLA hard limits
    if ai_result.get("priority") == "CRITICAL":
        ai_result["expectedResolutionHours"] = min(
            ai_result.get("expectedResolutionHours", 24),
            2
        )

    # 5️⃣ Sentiment-based escalation
    if (
        ai_result.get("sentiment") == "ANGRY"
        and ai_result.get("priority") != "CRITICAL"
    ):
        ai_result["priority"] = "HIGH"

    # 6️⃣ Final normalized response
    return {
        "category": ai_result.get("category", "UNKNOWN"),
        "confidence": confidence,
        "priority": ai_result.get("priority", "MEDIUM"),
        "urgency": ai_result.get("urgency", "NORMAL"),
        "sentiment": ai_result.get("sentiment", "NEUTRAL"),
        "expectedResolutionHours": ai_result.get("expectedResolutionHours", 24),
        "recommendedAction": ai_result.get(
            "recommendedAction", "AUTO_CLASSIFY"
        ),
        "requiresHumanReview": requires_human_review
    }
