from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import re
from ai_agent import SOCAiAgent
from slack_notifier import SlackNotifier

app = FastAPI(title="LogMind AI - Cloud Engine", version="1.0.0")

# API Key Security for Multi-Tenant SaaS
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Demo Valid API Keys (SaaS Database Table-এ সেভ থাকবে)
VALID_API_KEYS = {"client_secret_key_123", "client_secret_key_456"}

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Unauthorized API Key")
    return api_key

# Request Payload Schema
class LogPayload(BaseModel):
    ip: str
    url: str
    status_code: int = 200

# Initialize AI & Slack
ai_agent = SOCAiAgent()
slack = SlackNotifier()

# Detection Patterns
SQLI_PATTERN = re.compile(r"('|\"|%27|--|union\s+select|select\s+.*\s+from)", re.IGNORECASE)
CMDI_PATTERN = re.compile(r"(;|\|\||&&|\$\(.*\)|`.*`)", re.IGNORECASE)

@app.post("/api/v1/ingest", dependencies=[Depends(verify_api_key)])
async def ingest_log(log: LogPayload):
    threats = []
    
    if SQLI_PATTERN.search(log.url):
        threats.append("SQL Injection")
    if CMDI_PATTERN.search(log.url):
        threats.append("Command Injection")

    if not threats:
        return {"status": "clean", "message": "No threat detected"}

    # Threat Found -> Call AI Agent
    threat_str = ", ".join(threats)
    insight = ai_agent.analyze_threat(log.ip, log.url, threats)

    # Send Real-Time Slack Alert
    slack.send_threat_alert(log.ip, log.url, threat_str, insight)

    return {
        "status": "alert",
        "threats": threats,
        "ip": log.ip,
        "url": log.url,
        "ai_insight": insight
    }