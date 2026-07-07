import json
from semantic_kernel.contents.chat_history import ChatHistory

class EmailClassifierService:
    def __init__(self, kernel):
        self.kernel = kernel
        # Semantic Kernel se humara registered Gemini service nikal rahe hain
        self.chat_service = kernel.get_service()

    async def classify_email(self, sender: str, subject: str, body: str) -> dict:
        """
        Sends the email details to Google Gemini and returns a structured classification.
        """
        # Industrial prompt template focusing on zero shot classification and strict JSON structure
        prompt = f"""
You are an advanced AI Email Dispatcher. Your job is to analyze incoming emails and classify them accurately.

Analyze the following email details:
- From: {sender}
- Subject: {subject}
- Body Content: {body}

Choose exactly one of these categories:
1. SUPPORT: For technical problems, bugs, account issues, service center queries, or help requests.
2. INQUIRY: For general business questions, product details, feature inquiries, or pricing details.
3. SPAM: For newsletters, advertisements, system auto-alerts, or irrelevant marketing emails.

Provide your response in raw JSON format with exactly these keys:
- "category": (Strictly one of: "SUPPORT", "INQUIRY", "SPAM")
- "reason": (A precise 1-line explanation in English for why you chose this category)
- "priority": (Strictly one of: "HIGH", "MEDIUM", "LOW")

Response must be pure JSON only, without any markdown formatting wrappers like ```json or trailing text.
"""
        
        chat_history = ChatHistory()
        chat_history.add_user_message(prompt)

        try:
            # Hit the Gemini custom connector layer
            raw_response = await self.chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=None,
                kernel=self.kernel
            )
            
            # Clean response if it contains accidental markdown wrappers
            cleaned_response = raw_response.strip().replace("```json", "").replace("```", "").strip()
            
            # Parse response safely into dictionary
            result_json = json.loads(cleaned_response)
            return result_json
            
        except Exception as e:
            print(f"[ERROR] Classification failed for email from {sender}: {e}")
            return {
                "category": "SPAM",
                "reason": "Failed to parse AI output or process request, safely defaulting to SPAM.",
                "priority": "LOW"
            }