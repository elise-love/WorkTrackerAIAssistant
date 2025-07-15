# assistant/core/chat_client.py
from core.openai_client import chat_completion
from config import MODEL_DEFAULT
from mem.character_profile import build_system_prompt

def send(user_text, history: list[tuple[str,str]],profile_id: str ="Elfie")->str:
    system_prompt = build_system_prompt(profile_id)

    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": user_text})
    
    reply = chat_completion(messages, MODEL_DEFAULT)
    history.append(("user_text", reply))

    return reply

if __name__ == '__main__':
    send()