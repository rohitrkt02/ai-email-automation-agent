import asyncio
from app.kernel import create_agent_kernel
from semantic_kernel.contents.chat_history import ChatHistory

async def main():
    print("[TEST] Starting Semantic Kernel Test with Gemini...")
    
    # Initialize kernel
    kernel = create_agent_kernel()
    
    # Get the registered chat service
    chat_service = kernel.get_service()
    
    # Simple test prompt
    chat_history = ChatHistory()
    chat_history.add_user_message("Hello! If you are working perfectly, reply with 'Kernel Connected Successfully'.")
    
    print("[TEST] Sending test message to Gemini...")
    
    # Fetching response directly through our custom service layer
    response = await chat_service.get_chat_message_content(
        chat_history=chat_history,
        settings=None,
        kernel=kernel
    )
    
    print(f"\n[LLM RESPONSE]: {response}")
    print("\n[TEST] Semantic Kernel execution finished.")

if __name__ == "__main__":
    asyncio.run(main())