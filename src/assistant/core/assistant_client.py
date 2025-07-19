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
    if not user_input.strip():
        logging.warning("Failed to send: blank message")
        return "(Error: Please enter non-empty messages)"
    
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

    #count tokens
    usage = run_status.usage
    print(f"[Debug] usage object: {usage}")
    input_tokens = getattr(usage, 'prompt_tokens', 0)
    output_tokens = getattr(usage, 'completion_tokens', 0)
    tokens_used = input_tokens + output_tokens
    print(f"[Debug] Tokens used this run: {tokens_used}")

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE threads
            SET token_usage = token_usage + ?
            WHERE id =?
        ''',(tokens_used, thread_id))
        print(f"[Debug] Rows updated: {cursor.rowcount}")
        conn.commit()

    # Get assistant reply
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value
    return "(No assistant reply found)"

def read_thread_messages(thread_id: str):
    print("Chat History:\n")
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    for msg in reversed(messages.data):
        role = msg.role
        content_blocks = msg.content
        prefix = "芍芍" if role == "user" else "精靈"

        for block in content_blocks:
            if block.type == "text":
                print(f"{prefix}: {block.text.value.strip()}\n")

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT token_usage FROM threads WHERE id =?", (thread_id,))
        result = cursor.fetchone()
        if result:
            token_usage =result[0]
            print(f"Tokens Used in Total: {token_usage}")
        else:
            print("Thread not found in database.")

    print("\n\n")