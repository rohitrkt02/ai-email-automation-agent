from app.services.gmail_service import GmailService

if __name__ == "__main__":
    print("[TEST] Starting Gmail Integration Test...")
    
    # Initialize the Gmail Service (This will trigger OAuth if token doesn't exist)
    gmail = GmailService()
    
    print("\n[TEST] Fetching recent unread primary emails...")
    # Fetching maximum 3 unread emails from the last 1 day ('1d')
    emails = gmail.get_unread_emails(max_results=3, timeframe="1d")
    
    print(f"\n[TEST] Total unread emails found: {len(emails)}")
    
    for e in emails:
        print(f"\n--- Message ID: {e['id']} ---")
        print(f"From: {e['sender']}")
        print(f"Subject: {e['subject']}")
        print(f"Body Snippet: {e['body']}")
    
    print("\n[TEST] Gmail Integration Test execution finished.")