# assistant/message_builder.py
from config import SYSTEM_PROMPT 

def _build_messages(user_text: str, history: list[tuple[str,str]])->list[dict]:
        messages = [{"role":"system","content": SYSTEM_PROMPT}]

        for role, content in history:
            messages.append({"role": role, "content": content})

        # 最後再把最新的 user_text 加入
        messages.append({"role":"user","content":user_text})
        return messages

if __name__ == '__main__':
    _build_messages()