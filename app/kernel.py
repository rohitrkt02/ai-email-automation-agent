import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.text_completion_client_base import TextCompletionClientBase

load_dotenv()

class GeminiCustomService(TextCompletionClientBase):
    def __init__(self, ai_model_id: str, api_key: str):
        super().__init__(ai_model_id=ai_model_id, service_id="gemini_custom")
        from google import genai
        self.__dict__['client'] = genai.Client(api_key=api_key)
        self.__dict__['model_name'] = ai_model_id

    async def get_chat_message_content(self, chat_history, settings=None, kernel=None):
        prompt = chat_history.messages[-1].content
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        return response.text

    async def get_text_contents(self, prompt: str, settings=None, kernel=None):
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        return [response.text]

    async def get_streaming_text_contents(self, prompt: str, settings=None, kernel=None):
        pass

class KernelManager:
    def __init__(self):
        self.kernel = Kernel()
        self._configure_services()
        self._register_native_plugins() # Load Phase 10 Plugins

    def _configure_services(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: 'GEMINI_API_KEY' is missing.")

        chat_service = GeminiCustomService(ai_model_id="gemini-2.5-flash", api_key=api_key)
        self.kernel.add_service(chat_service)
        print("[INFO] Semantic Kernel successfully bridged with Google Gemini Service.")

    def _register_native_plugins(self):
        """Imports and registers native functional plugins inside the orchestrator lifecycle."""
        from app.plugins.gmail_plugin import GmailPlugin
        from app.plugins.processing_plugin import EmailProcessingPlugin

        # Register Plugins into the Kernel
        self.kernel.add_plugin(GmailPlugin(), plugin_name="GmailPlugin")
        self.kernel.add_plugin(EmailProcessingPlugin(self.kernel), plugin_name="EmailProcessingPlugin")
        print("[INFO] Native Semantic Kernel Plugins successfully imported and registered.")

    def get_kernel(self) -> Kernel:
        return self.kernel

def create_agent_kernel() -> Kernel:
    manager = KernelManager()
    return manager.get_kernel()