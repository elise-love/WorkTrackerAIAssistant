# assistant/core/chat_client.py
from core.openai_client import chat_completion
from config import MODEL_DEFAULT
from mem.character_profile import build_system_prompt
import re

def send(user_text, history: list[tuple[str,str]],profile_id: str ="Elfie")->tuple[str,str]:
    system_prompt = build_system_prompt(profile_id, mode='live')

    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": user_text})
    
    full_response = chat_completion(messages, MODEL_DEFAULT)
    response , category = extract_response_and_category(full_response)
    history.append((user_text, response))

    return response,category

def extract_response_and_category(full_response: str)->tuple[str, str]:
        match = re.search(r'#CATEGORY:(\w+)', full_response)
        if match:
            category = match.group(1).lower()
            response = full_response.replace(match.group(0),'').strip()
        else:
            category = "uncategorized"
            response = full_response.strip()

        return response, category



if __name__ == '__main__':
    send()