import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_ticket(ticket_text: str):
    prompt = f"""
You are an AI system supporting a BPM workflow engine.

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You return structured decisions for workflows."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()
