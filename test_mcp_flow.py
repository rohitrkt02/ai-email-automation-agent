import asyncio
from app.kernel import create_agent_kernel
from app.services.classifier_service import EmailClassifierService
from app.services.summarizer_service import EmailSummarizerService

async def main():
    print("[TEST] Starting Phase 8 & 9 - MCP Tool & Filesystem Verification...")
    
    kernel = create_agent_kernel()
    classifier = EmailClassifierService(kernel)
    summarizer = EmailSummarizerService(kernel)
    
    # Mock Data for verification
    sender = "test@domain.com"
    subject = "Urgent Server Migration Pending"
    body = "Hi, please note that the main database migration is scheduled for tonight at 12:00 AM. Stop all write operations."

    print("\n[AI] Running Classifier using MCP Prompt Loading...")
    cls_res = await classifier.classify_email(sender, subject, body)
    print(f"📊 Result: {cls_res}")

    print("\n[AI] Running Summarizer using MCP Prompt Loading...")
    sum_res = await summarizer.summarize_email(sender, subject, body)
    print(f"📝 Result: {sum_res}")
    
    print("\n[SUCCESS] Phase 8 & 9 MCP testing complete!")

if __name__ == "__main__":
    asyncio.run(main())