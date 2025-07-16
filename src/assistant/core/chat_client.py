from core.openai_client import chat_completion
from config import MODEL_DEFAULT, ASSISTANT_PROMPT_ID

def send(user_text, history: list[tuple[str, str]], profile_id: str = "Elfie") -> str:
    messages = []
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": user_text})

    assistant_text = chat_completion(
        messages=messages,
        model=MODEL_DEFAULT,
        prompt_id=ASSISTANT_PROMPT_ID,
    )

    history.append((user_text, assistant_text))
    return assistant_text
