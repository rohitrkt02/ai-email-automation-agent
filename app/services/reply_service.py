from semantic_kernel.contents.chat_history import ChatHistory

class EmailReplyService:
    def __init__(self, kernel):
        self.kernel = kernel
        self.chat_service = kernel.get_service()

    async def generate_reply(self, priority: str, reason: str, summary: str, sender: str, subject: str, body: str) -> str:
        """
        Generates a professional, targeted response using classification context.
        As per Phase 7 Roadmap Requirements.
        """
        prompt = f"""
You are an expert Email Assistant. Draft a professional, friendly, and short email reply based on the input context.

Context Details:
- Original Email From: {sender}
- Subject: {subject}
- Email Body: {body}
- Assigned Priority: {priority}
- AI Logic Reason: {reason}
- Content Summary: {summary}

Instructions:
1. Keep the email precise and short.
2. Ensure there is absolute zero hallucination (do not invent numbers, contact links, or fake office locations).
3. Sign off strictly as:
   Regards,
   Rohit (AI Assistant)

Provide ONLY the final email body content. Do not include markdown backticks or extra text.
"""
        chat_history = ChatHistory()
        chat_history.add_user_message(prompt)

        try:
            reply_content = await self.chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=None,
                kernel=self.kernel
            )
            return reply_content.strip()
        except Exception as e:
            print(f"[ERROR] Reply draft generation failed: {e}")
            return f"Hello,\n\nThank you for reaching out. We have received your email and are looking into it.\n\nRegards,\nRohit (AI Assistant)"