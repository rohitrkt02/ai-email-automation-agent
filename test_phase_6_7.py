import asyncio
from app.services.gmail_service import GmailService
from app.kernel import create_agent_kernel
from app.services.classifier_service import EmailClassifierService
from app.services.summarizer_service import EmailSummarizerService
from app.services.reply_service import EmailReplyService

async def main():
    print("[TEST] Starting Phase 6 (Summarizer) & Phase 7 (Reply Generator) Combo Test...")
    
    # Initialize Core Setup
    gmail_service = GmailService()
    kernel = create_agent_kernel()
    
    classifier = EmailClassifierService(kernel)
    summarizer = EmailSummarizerService(kernel)
    reply_service = EmailReplyService(kernel)
    
    print("[INFO] Scanning for unread primary emails...")
    unread_emails = gmail_service.get_unread_emails(max_results=1, timeframe="1d")
    
    if not unread_emails:
        print("[INFO] Primary inbox is empty. Injecting Mock Corporate Request for validation...")
        unread_emails = [{
            'id': 'mock_comb_999',
            'sender': 'hr@deloitte.com',
            'subject': 'Java-Fresher Internship Orientation Schedule',
            'body': 'Hi Rohit, congratulations on clearing the technical round. Your formal orientation is scheduled for next Friday at 10:00 AM. Please reply by this evening confirming your available documents including your current B.Tech marksheet and caste certificate for application processing.'
        }]

    for email in unread_emails:
        print(f"\n==========================================")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"==========================================")
        
        # 1. Run Phase 5 - Classification
        print("\n[AI] Running Phase 5 (Classifier)...")
        classification = await classifier.classify_email(email['sender'], email['subject'], email['body'])
        priority = classification.get('priority', 'Low')
        reason = classification.get('reason', 'N/A')
        print(f"📊 Priority: {priority} | Reason: {reason}")
        
        # 2. Run Phase 6 - Summarization
        print("\n[AI] Running Phase 6 (Summarizer)...")
        summary_data = await summarizer.summarize_email(email['sender'], email['subject'], email['body'])
        print(f"📝 Summary: {summary_data.get('summary')}")
        print(f"⏳ Deadline: {summary_data.get('deadline')}")
        print(f"🎯 Action Items: {summary_data.get('action_items')}")
        
        # 3. Run Phase 7 - Reply Generation
        print("\n[AI] Running Phase 7 (Reply Draft Generator)...")
        reply_draft = await reply_service.generate_reply(
            priority=priority,
            reason=reason,
            summary=summary_data.get('summary'),
            sender=email['sender'],
            subject=email['subject'],
            body=email['body']
        )
        print(f"\n✨ [GENERATED REPLY DRAFT]:\n{reply_draft}")
        print("==========================================")

if __name__ == "__main__":
    asyncio.run(main())