import os
from datetime import datetime
from dotenv import load_dotenv

# Absolute path allocation
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Direct extraction check
DATABASE_URL = os.getenv("DATABASE_URL")

# IF STILL NOT FOUND, FORCE HARDCODE AS FALLBACK FOR TESTING
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:7860220452%26rohit@localhost:5432/email_agent_db"

# Initialize connection engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== ORM MODELS ====================

class ProcessedEmail(Base):
    __tablename__ = 'processed_emails'
    
    email_id = Column(String(100), primary_key=True)
    sender = Column(String(255), nullable=False)
    subject = Column(String(255))
    priority = Column(String(50))
    summary = Column(Text)
    processed_at = Column(DateTime, default=datetime.utcnow)

class SentReply(Base):
    __tablename__ = 'sent_replies'
    
    id = Column(String(100), primary_key=True)
    email_id = Column(String(100), nullable=False)
    recipient = Column(String(255), nullable=False)
    reply_body = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

class SystemLog(Base):
    __tablename__ = 'system_logs'
    
    id = Column(String(100), primary_key=True, default=lambda: str(datetime.utcnow().timestamp()))
    log_level = Column(String(50))
    module = Column(String(100))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ==================== HELPER MANAGER ====================

class DatabaseManager:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def get_session(self):
        return SessionLocal()

    def log_email(self, email_id: str, sender: str, subject: str, priority: str, summary: str):
        session = self.get_session()
        try:
            record = ProcessedEmail(
                email_id=email_id, sender=sender, subject=subject, priority=priority, summary=summary
            )
            session.merge(record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"[DB ERROR] Failed to log email: {e}")
        finally:
            session.close()

    def is_email_processed(self, email_id: str) -> bool:
        session = self.get_session()
        exists = session.query(ProcessedEmail).filter(ProcessedEmail.email_id == email_id).first() is not None
        session.close()
        return exists