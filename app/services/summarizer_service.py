import json
from semantic_kernel.contents.chat_history import ChatHistory
from app.mcp.mcp_server import MCPServer

class EmailSummarizerService:
    """
    Extracts summary, action items and deadlines using filesystem schemas via MCP.
    As per Phase 6, 8 & 9 Roadmap Requirements.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.chat_service = kernel.get_service()
        self.mcp = MCPServer()  # Injecting MCP Server Tools

    async def summarize_email(self, sender: str, subject: str, body: str) -> dict:
        # Load prompt template dynamically using MCP Tool
        template = self.mcp.load_prompt("summary")
        prompt = template.format(sender=sender, subject=subject, body=body)
        
        chat_history = ChatHistory()
        chat_history.add_user_message(prompt)

        try:
            raw_response = await self.chat_service.get_chat_message_content(chat_history=chat_history)
            cleaned_response = raw_response.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_response)
        except Exception as e:
            self.mcp.save_log("error", f"Summarization failed: {e}")
            return {
                "summary": "Fallback activated.",
                "action_items": [],
                "deadline": "None Specified",
                "important_points": []
            }