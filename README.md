AI Ticket Decision API

A lightweight AI-powered decision microservice that analyzes support tickets and returns structured workflow decisions for Flowable BPMN processes.

The service evaluates ticket priority, category, urgency, sentiment, SLA, and escalation recommendations using a Groq-hosted LLM.

Features

AI-based ticket priority classification

Issue category detection (payment, login, security, etc.)

Sentiment analysis for escalation handling

SLA prediction (expected resolution time)

Confidence-based governance (human review fallback)

Designed for Flowable / BPM integration

API Endpoint
POST /prioritize

Evaluates a support ticket and returns workflow decisions.

python -m venv .venv
source .venv/Scripts/activate
