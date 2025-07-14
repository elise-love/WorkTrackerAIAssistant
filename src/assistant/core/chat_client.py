# assistant/core/chat_client.py
from core.message_builder import _build_messages
from core.openai_client import chat_completion
from config import MODEL_DEFAULT

def send(user_text, history: list[tuple[str,str]])->str:
    messages = _build_messages(user_text, history)
    reply = chat_completion(messages, MODEL_DEFAULT)

    # OpenAI 只會返回 assistant 角色
    history.append(("assistant", reply))
    return reply

if __name__ == '__main__':
    send()