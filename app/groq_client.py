import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_ticket(ticket_text: str) -> str:
    prompt = f"""
You are an AI decision engine for a BPM workflow system.

Analyze the support ticket and return ONLY valid JSON with:
priority: LOW | MEDIUM | HIGH | CRITICAL
category: PAYMENT | LOGIN | PERFORMANCE | SECURITY | DATA | FEATURE | OTHER
urgency: LOW | NORMAL | IMMEDIATE
sentiment: CALM | NEUTRAL | FRUSTRATED | ANGRY
expectedResolutionHours: number
recommendedAction: AUTO_ASSIGN | ESCALATE_L2 | ESCALATE_L3 | MANUAL_REVIEW

Ticket:
{ticket_text}

Return ONLY JSON. No explanation.
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Return structured JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return completion.choices[0].message.content.strip()
