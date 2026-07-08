import json
from semantic_kernel.contents.chat_history import ChatHistory
from app.mcp.mcp_server import MCPServer

class EmailClassifierService:
    """
    Classifies incoming emails based on strict structural prompt mapping via MCP.
    As per Phase 5, 8 & 9 Roadmap Requirements.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.chat_service = kernel.get_service()
        self.mcp = MCPServer()  # Injecting MCP Server Tools

    async def classify_email(self, sender: str, subject: str, body: str) -> dict:
        # Load prompt template dynamically using MCP Tool
        template = self.mcp.load_prompt("priority")
        prompt = template.format(sender=sender, subject=subject, body=body)
        
        chat_history = ChatHistory()
        chat_history.add_user_message(prompt)

        try:
            raw_response = await self.chat_service.get_chat_message_content(chat_history=chat_history)
            cleaned_response = raw_response.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_response)
        except Exception as e:
            self.mcp.save_log("error", f"Classification failed: {e}")
            return {"priority": "Low", "reason": "MCP fallback triggered due to internal exception."}