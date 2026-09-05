import os
import sys

# Current script path and src path setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Direct local imports
from rule_engine import RuleEngine
from ai_agent import AIAgent
from slack_notifier import SlackNotifier
from database import engine, Base, get_db
import models

# Automatically create tables in PostgreSQL on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LogMind AI SaaS Engine")

# Security API Key setup
API_KEY = os.getenv("API_KEY", "client_secret_key_123")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return api_key

# Initialize core services
rule_engine = RuleEngine()
ai_agent = AIAgent()
slack = SlackNotifier()

# Request Pydantic model
class LogIngest(BaseModel):
    ip: str
    url: str
    status_code: int

@app.get("/")
def read_root():
    return {"message": "LogMind AI Engine is active"}

@app.post("/api/v1/ingest")
def ingest_log(log: LogIngest, api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    threats = rule_engine.analyze(log.url)
    
    threat_str = None
    insight_text = None
    
    if threats:
        threat_str = ", ".join(threats)
        insight = ai_agent.analyze_threat(log.ip, log.url, threats)
        insight_text = str(insight) if insight else "Potential threat detected."
        
        slack.send_threat_alert(log.ip, log.url, threat_str, insight_text)

    db_log = models.SecurityLog(
        ip=log.ip,
        url=log.url,
        status_code=log.status_code,
        threat_type=threat_str,
        ai_insight=insight_text
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {
        "status": "success", 
        "threats": threats, 
        "log_id": db_log.id
    }

@app.get("/api/v1/alerts")
def get_all_alerts(api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    alerts = db.query(models.SecurityLog).filter(models.SecurityLog.threat_type.isnot(None)).all()
    return {
        "total_alerts": len(alerts), 
        "data": alerts
    }