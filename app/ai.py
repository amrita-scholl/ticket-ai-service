import os
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read API key from environment properly
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt: str) -> str:
    result = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract message content correctly
    return result.choices[0].message.content
