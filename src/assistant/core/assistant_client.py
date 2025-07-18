from openai import OpenAI
from datetime import datetime
from db import connect
from config import OPENAI_API_KEY, OPENAI_ORG_ID, ASSISTANT_ID
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

def create_thread(title: str = "unnamed chat", category: str = "uncategorized") -> str:
    thread = client.beta.threads.create()
    thread_id = thread.id
    created_at = datetime.now().isoformat()

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO threads (id, assistant_id, title, category, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (thread_id, ASSISTANT_ID, title, category, created_at))
        conn.commit()

    logging.info(f"New thread created: {thread_id}")
    return thread_id

def send_message_to_thread(thread_id: str, user_input: str) -> str:
    # Append user input to thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
    )

    # Activate assistant run
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            logging.error(f" Run failed with status: {run_status.status}")
            return "(Run failed)"
        time.sleep(1)

    # Get assistant reply
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in reversed(messages.data):
        if message.role == "assistant":
            return message.content[0].text.value
    return "(No assistant reply found)"

def read_thread_messages(thread_id: str):
    print("Chat History:\n")
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    for msg in reversed(messages.data):
        role = msg.role
        content_blocks = msg.content
        prefix = "User" if role == "user" else "Elfie"

        for block in content_blocks:
            if block.type == "text":
                print(f"{prefix}:\n{block.text.value.strip()}\n")
