import asyncio
from app.services.gmail_service import GmailService
from app.kernel import create_agent_kernel
from app.services.classifier_service import EmailClassifierService

async def main():
    print("[TEST] Starting Live Email Classification Test...")
    
    # 1. Initialize Gmail Service & Fetch 2 latest unread primary emails
    gmail_service = GmailService()
    print("[TEST] Fetching unread emails from primary inbox...")
    unread_emails = gmail_service.get_unread_emails(max_results=2, timeframe="1d")
    
    if not unread_emails:
        print("[INFO] Primary inbox me pichle 24 hours me koi unread email nahi mili.")
        print("[INFO] Mock execution test chala rahe hain testing check karne ke liye...\n")
        
        # Mock Email for testing if inbox is empty
        unread_emails = [{
            'id': 'mock_123',
            'sender': 'support@dell-india.com',
            'subject': 'Laptop keyboard heating issue - Ticket #4910',
            'body': 'My Inspiron laptop keyboard is overheating within 10 minutes of usage. Please update my service status.'
        }]

    # 2. Initialize Semantic Kernel & Classifier Service
    kernel = create_agent_kernel()
    classifier = EmailClassifierService(kernel)
    
    # 3. Process & Classify each email
    for email in unread_emails:
        print(f"\n--- Processing Email ID: {email['id']} ---")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        
        print("[TEST] Sending to Gemini Classifier Engine...")
        classification = await classifier.classify_email(
            sender=email['sender'],
            subject=email['subject'],
            body=email['body']
        )
        
        print("\n[AI CLASSIFICATION RESULT]:")
        print(f"📊 Category: {classification.get('category')}")
        print(f"🚨 Priority: {classification.get('priority')}")
        print(f"📝 Reason: {classification.get('reason')}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())