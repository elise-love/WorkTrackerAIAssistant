# openai_client.py
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_ORG_ID, ASSISTANT_ID, THREAD_ID
import time

client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

def run_assistant(user_input: str) -> str:
    # 建立一個新的 thread（避免用舊 thread）
    thread = client.beta.threads.create()
    
    # 傳送訊息
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    # 啟動 assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            raise RuntimeError(f"Run failed with status: {run_status.status}")
        time.sleep(0.5)

    # 取得回覆
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in reversed(messages.data):
        if message.role == "assistant":
            return message.content[0].text.value

    return "(No assistant reply found)"
