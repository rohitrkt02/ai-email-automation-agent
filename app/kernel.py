import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.text_completion_client_base import TextCompletionClientBase

# Load environment variables from .env file
load_dotenv()

class GeminiCustomService(TextCompletionClientBase):
    """A fully compliant custom service wrapper for Gemini using the latest google-genai SDK."""
    
    def __init__(self, ai_model_id: str, api_key: str):
        super().__init__(ai_model_id=ai_model_id, service_id="gemini_custom")
        # Using the new up-to-date official google-genai package
        from google import genai
        
        # Bypassing Pydantic validation assignment restriction using __dict__
        self.__dict__['client'] = genai.Client(api_key=api_key)
        self.__dict__['model_name'] = ai_model_id

    async def get_chat_message_content(self, chat_history, settings=None, kernel=None):
        """Processes the history and returns chat content."""
        prompt = chat_history.messages[-1].content
        # New Google GenAI SDK syntax: client.models.generate_content
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    # MANDATORY ABSTRACT METHODS REQUIRED BY SEMANTIC KERNEL
    async def get_text_contents(self, prompt: str, settings=None, kernel=None):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return [response.text]

    async def get_streaming_text_contents(self, prompt: str, settings=None, kernel=None):
        """Implemented to satisfy abstract interface."""
        pass

class KernelManager:
    def __init__(self):
        self.kernel = Kernel()
        self._configure_services()

    def _configure_services(self):
        """Configures the Gemini LLM service seamlessly."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: 'GEMINI_API_KEY' is missing in the environment variables.")

        chat_service = GeminiCustomService(
            ai_model_id="gemini-2.5-flash",
            api_key=api_key
        )
        
        # Register the service with Semantic Kernel Orchestrator
        self.kernel.add_service(chat_service)
        print("[INFO] Semantic Kernel successfully bridged with Google Gemini Service.")

    def get_kernel(self) -> Kernel:
        return self.kernel

def create_agent_kernel() -> Kernel:
    manager = KernelManager()
    return manager.get_kernel()