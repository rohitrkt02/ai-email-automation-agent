import json
from semantic_kernel.contents.chat_history import ChatHistory

class EmailSummarizerService:
    def __init__(self, kernel):
        self.kernel = kernel
        self.chat_service = kernel.get_service()

    async def summarize_email(self, sender: str, subject: str, body: str) -> dict:
        """
        Analyzes long emails and returns structured summary, action items, and deadlines.
        As per Phase 6 Roadmap Requirements.
        """
        prompt = f"""
You are an expert Executive Assistant. Your job is to read long or short emails and provide a structured summary.

Analyze the following email:
- From: {sender}
- Subject: {subject}
- Body: {body}

Extract the details and provide your response in raw JSON format with exactly these keys:
- "summary": (A clear 1-2 sentence overview of the email content)
- "action_items": (A Python list/array of explicit tasks or next steps expected from us)
- "deadline": (Any specific date/time mentioned, or "None Specified" if not found)
- "important_points": (A Python list/array of key insights, facts, or critical highlights)

Response must be pure JSON only, without any markdown formatting wrappers like ```json or trailing text.
"""
        chat_history = ChatHistory()
        chat_history.add_user_message(prompt)

        try:
            raw_response = await self.chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=None,
                kernel=self.kernel
            )
            
            cleaned_response = raw_response.strip().replace("```json", "").replace("```", "").strip()
            result_json = json.loads(cleaned_response)
            return result_json
            
        except Exception as e:
            print(f"[ERROR] Summarization failed for email from {sender}: {e}")
            return {
                "summary": "Failed to generate summary due to processing exception.",
                "action_items": [],
                "deadline": "None Specified",
                "important_points": []
            }