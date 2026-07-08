import os
from app.utils.logger import agent_logger

def main():
    print("[TEST] Starting Phase 13 - Production Logger Simulation Audit...")
    
    # Simulating industrial transaction steps using our new logging engine
    agent_logger.info("Initializing automated email scanner daemon workflow.")
    agent_logger.info("Gmail API fetched 3 unread primary emails successfully.")
    agent_logger.warning("Gemini processing safety latency detected but handled.")
    agent_logger.error("Database connection pooling fallback triggered (Mock Error Simulation).")
    
    # Paths verification check
    base_dir = os.path.dirname(os.path.abspath(__file__))
    expected_log_path = os.path.join(base_dir, 'logs', 'agent_pipeline.log')
    
    print("\n--- Verifying Log File Creation on Filesystem ---")
    if os.path.exists(expected_log_path):
        print(f"[SUCCESS] Log file found at: {expected_log_path}")
        print("--- Last 2 Lines from the live log file ---")
        with open(expected_log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-2:]:
                print(line.strip())
        print("\n[SUCCESS] Phase 13 - Logging Engine verified 100%!")
    else:
        print("[CRITICAL ERROR] Logging engine failed to write to physical directory structure.")

if __name__ == "__main__":
    main()