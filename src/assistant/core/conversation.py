"""
這支檔案負責把「系統提示 + 對話歷史 + 使用者新輸入」組成
#OpenAI API 要求的 messages 格式。

1.使用者輸入 user_text，你呼叫 send(...)

2.它叫 conversation._build_messages(...) 把訊息包成 OpenAI 格式

3.它再叫 openai_client.chat_completion(...) 丟給 OpenAI API

4.拿到回應後 append 回 history，讓上下文延續

5.回傳回應文字給使用端
"""
# assistant/conversation.py
from assistant.config import SYSTEM_PROMPT # 從 config.py 匯入系統提示文字

def _build_messages(user_text: str, history: list[tuple[str,str]])->list[dict]:
        messages = [{"role":"system","content": SYSTEM_PROMPT}]

        for role, content in history:
            messages.append({"role": role, "content": content})

        # 最後再把最新的 user_text 加入
        messages.append({"role":"user","content":user_text})
        return messages# 回傳組好的 list，給 chat_client 使用

