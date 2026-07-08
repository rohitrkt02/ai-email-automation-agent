import os

class MCPServer:
    """
    Model Context Protocol (MCP) inspired local tool server for Filesystem management.
    As per Phase 8 & 9 Roadmap requirements.
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.prompts_dir = os.path.join(self.base_dir, 'prompts')
        self.logs_dir = os.path.join(self.base_dir, 'logs')
        
        # Ensure directories exist
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

    def load_prompt(self, template_name: str) -> str:
        """TOOL: Reads a prompt from the filesystem template repository."""
        file_path = os.path.join(self.prompts_dir, f"{template_name}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"[MCP ERROR] Template '{template_name}.txt' not found at {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def save_reply_draft(self, email_id: str, draft_content: str):
        """TOOL: Writes generated draft to the local filesystem for history tracking."""
        drafts_dir = os.path.join(self.base_dir, 'data', 'drafts')
        os.makedirs(drafts_dir, exist_ok=True)
        
        file_path = os.path.join(drafts_dir, f"{email_id}_reply.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(draft_content)
        print(f"[MCP TOOL] Successfully saved draft to filesystem for Email ID: {email_id}")

    def save_log(self, log_type: str, message: str):
        """TOOL: Appends real-time pipeline telemetry logs to file."""
        log_file = os.path.join(self.logs_dir, f"{log_type}.log")
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(f"{message}\n")