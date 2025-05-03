"""
Imports openai, sets the key from config.py, chooses model names, handles retries & error mapping.
Count tokens, catch RateLimitError, write to a log file.
只負責「聊」，不直接打 API
"""
#chat_client.py
from assistant.core.openai_client import chat_completion
from assistant.config import MODEL_DEFAULT

def send(user_text, history):
    messages = _build_messages(user_text, history)
    reply = chat_completion(messages, MODEL_DEFAULT)
    history.append(("assistant", reply))
    return reply
