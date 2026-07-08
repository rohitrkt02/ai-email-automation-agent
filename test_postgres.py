import asyncio
import os
from dotenv import load_dotenv

# Force clear context and reload for verification
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

from app.services.db_service import DatabaseManager

async def main():
    print("[TEST] Starting Phase 11 - PostgreSQL Connection & Schema Audit...")
    
    # Check what keys are actually being read from .env
    print(f"[DEBUG] Available keys in os.environ: {list(os.environ.keys())[:5]}... (showing top 5)")
    print(f"[DEBUG] Raw DATABASE_URL read test: {os.getenv('DATABASE_URL')}")
    
    try:
        db = DatabaseManager()
        print("[SUCCESS] Connected to PostgreSQL. Tables auto-synced successfully!")
        
        test_id = "mock_db_test_999"
        if not db.is_email_processed(test_id):
            db.log_email(
                email_id=test_id,
                sender="audit@deloitte.com",
                subject="Postgres Integration Complete",
                priority="Medium",
                summary="System verified connectivity parameters securely."
            )
            print("[SUCCESS] Data write test completed successfully!")
        else:
            print("[INFO] Email already exists in memory registry.")
            
        assert db.is_email_processed(test_id) == True
        print("\n[SUCCESS] Phase 11 - PostgreSQL Memory Architecture setup verified 100%!")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Database integration failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())