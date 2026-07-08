import asyncio
import json
from app.kernel import create_agent_kernel

async def main():
    print("[TEST] Starting Phase 10 - Semantic Kernel Native Plugins Orchestration Test...")
    
    # 1. Initialize Kernel with plugins autoloaded
    kernel = create_agent_kernel()
    
    # Mock Email structure
    sender = "interviews@hcl.com"
    subject = "Urgent: HCL Internship Shortlist Updates"
    body = "Hi Rohit, your profile has been selected for the next round. Please reply with your confirmation as soon as possible."

    # 2. Extract registered functions from the kernel
    processing_plugin = kernel.get_plugin(plugin_name="EmailProcessingPlugin")
    classify_func = processing_plugin["classify_email_urgency"]
    summarize_func = processing_plugin["summarize_email_content"]
    reply_func = processing_plugin["generate_auto_reply_draft"]

    # 3. Invoke Classification through Kernel
    print("\n[KERNEL INVOCATION] Executing Classify Function...")
    cls_result_str = await kernel.invoke(classify_func, sender=sender, subject=subject, body=body)
    cls_data = json.loads(str(cls_result_str))
    print(f"📊 Plugin Output -> Priority: {cls_data.get('priority')}")

    # 4. Invoke Summarization through Kernel
    print("\n[KERNEL INVOCATION] Executing Summarize Function...")
    sum_result_str = await kernel.invoke(summarize_func, sender=sender, subject=subject, body=body)
    sum_data = json.loads(str(sum_result_str))
    print(f"📝 Plugin Output -> Summary: {sum_data.get('summary')}")

    # 5. Invoke Reply Draft through Kernel
    print("\n[KERNEL INVOCATION] Executing Reply Generator Function...")
    reply_result = await kernel.invoke(
        reply_func,
        priority=cls_data.get('priority'),
        reason=cls_data.get('reason'),
        summary=sum_data.get('summary'),
        sender=sender,
        subject=subject,
        body=body
    )
    print(f"\n✨ [PLUGIN GENERATED DRAFT]:\n{reply_result}")
    print("\n[SUCCESS] Phase 10 Plugin architecture verified completely!")

if __name__ == "__main__":
    asyncio.run(main())