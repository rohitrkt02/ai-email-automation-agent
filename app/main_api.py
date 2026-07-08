import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.services.db_service import DatabaseManager, ProcessedEmail, SentReply, SystemLog

# Initialize FastAPI App with clean Swagger Metadata
app = FastAPI(
    title="AI Email Automation Agent Dashboard API",
    description="REST API Endpoints to monitor classification metrics and handle manual hooks.",
    version="1.0.0"
)

# Initialize DB Manager
db_manager = DatabaseManager()

# Dependency to get db session safely per request
def get_db():
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()

# ==================== PYDANTIC SCHEMAS ====================
class EmailResponseSchema(BaseModel):
    email_id: str
    sender: str
    subject: str
    priority: str
    summary: str

    class Config:
        from_attributes = True

class ManualReplyRequest(BaseModel):
    to_email: str
    subject: str
    body: str
    thread_id: str

# ==================== API ENDPOINTS ====================

@app.get("/", tags=["Root"])
def root_check():
    """Health check endpoint to ensure API layer is online."""
    return {"status": "ONLINE", "agent": "Semantic-Kernel-Postgres-Agent"}

@app.get("/emails", response_model=List[EmailResponseSchema], tags=["Email Analytics"])
def get_processed_emails(limit: int = 10, db: Session = Depends(get_db)):
    """
    ROADMAP FEATURE: GET /emails
    Fetches the history of classified and summarized emails from PostgreSQL.
    """
    emails = db.query(ProcessedEmail).order_by(ProcessedEmail.processed_at.desc()).limit(limit).all()
    return emails

@app.post("/reply", tags=["Manual Actions"])
def send_manual_reply(payload: ManualReplyRequest):
    """
    ROADMAP FEATURE: POST /reply
    Allows an admin or user to bypass auto-pilot and send a direct manual reply via Gmail API.
    """
    from app.services.gmail_service import GmailService
    try:
        gmail = GmailService()
        result = gmail.send_reply(
            to_email=payload.to_email,
            subject=payload.subject,
            body=payload.body,
            thread_id=payload.thread_id
        )
        if result:
            return {"status": "SUCCESS", "message": f"Reply successfully dispatched to {payload.to_email}"}
        raise HTTPException(status_code=500, detail="Gmail service failed to dispatch email.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs", tags=["System Telemetry"])
def get_system_audit_logs(limit: int = 5, db: Session = Depends(get_db)):
    """Fetches real-time transaction telemetry from Postgres storage."""
    logs = db.query(SystemLog).order_by(SystemLog.timestamp.desc()).limit(limit).all()
    return [{"module": log.module, "message": log.message, "time": log.timestamp} for log in logs]

# Utility script runner configuration
def start_api_server():
    uvicorn.run("app.main_api.py:app" if __name__ == "__main__" else "app.main_api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)