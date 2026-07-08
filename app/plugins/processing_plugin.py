import json
from semantic_kernel.functions import kernel_function
from app.services.classifier_service import EmailClassifierService
from app.services.summarizer_service import EmailSummarizerService
from app.services.reply_service import EmailReplyService

class EmailProcessingPlugin:
    def __init__(self, kernel):
        self.kernel = kernel
        self.classifier = EmailClassifierService(kernel)
        self.summarizer = EmailSummarizerService(kernel)
        self.reply_generator = EmailReplyService(kernel)

    @kernel_function(
        name="classify_email_urgency",
        description="Analyzes email headers/body and determines priority (Urgent, High, Medium, Low)."
    )
    async def classify_email_urgency(self, sender: str, subject: str, body: str) -> str:
        res = await self.classifier.classify_email(sender, subject, body)
        return json.dumps(res)

    @kernel_function(
        name="summarize_email_content",
        description="Extracts deep summary, action items and deadlines from the email."
    )
    async def summarize_email_content(self, sender: str, subject: str, body: str) -> str:
        res = await self.summarizer.summarize_email(sender, subject, body)
        return json.dumps(res)

    @kernel_function(
        name="generate_auto_reply_draft",
        description="Drafts a clean, short, professional response without hallucinations."
    )
    async def generate_auto_reply_draft(self, priority: str, reason: str, summary: str, sender: str, subject: str, body: str) -> str:
        reply = await self.reply_generator.generate_reply(priority, reason, summary, sender, subject, body)
        return reply