from semantic_kernel.functions import kernel_function
from app.services.gmail_service import GmailService

class GmailPlugin:
    def __init__(self):
        self.gmail_service = GmailService()

    @kernel_function(
        name="fetch_unread_emails",
        description="Fetches unread primary emails from Gmail inbox within a given timeframe."
    )
    def fetch_unread_emails(self, max_results: int = 5, timeframe: str = "1d") -> str:
        import json
        emails = self.gmail_service.get_unread_emails(max_results=max_results, timeframe=timeframe)
        return json.dumps(emails)

    @kernel_function(
        name="send_email_reply",
        description="Sends an automated reply inside a specific email thread."
    )
    def send_email_reply(self, to_email: str, subject: str, body: str, thread_id: str) -> str:
        result = self.gmail_service.send_reply(to_email, subject, body, thread_id)
        if result:
            return f"Successfully sent reply to {to_email}."
        return f"Failed to send reply to {to_email}."