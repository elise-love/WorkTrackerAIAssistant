"""
這支檔案負責把「系統提示 + 對話歷史 + 使用者新輸入」組成
#OpenAI API 要求的 messages 格式。
"""
# assistant/conversation.py
from assistant.config import SYSTEM_PROMPT # 從 config.py 匯入系統提示文字


"""
    將 (role, content) 的 tuple list 轉成 OpenAI API 需要的 list[dict]，
    並在最前面插入 SYSTEM_PROMPT、最後面插入最新 user_text。
    
    參數
    ----
    user_text : str
        使用者最新輸入的文字。
    history : list[tuple[str, str]]
        歷史對話，形式是 [(role, content), ...]，
        role 只能是 "user" 或 "assistant"。

    回傳
    ----
    list[dict]
        每個元素都是 {"role": ..., "content": ...}，符合 API 規格。
"""
def _build_messages(user_text: str, history: list[tuple[str,str]])->list[dict]:
        messages = [{"role":"system","content": SYSTEM_PROMPT}]

        for role, content in history:
            messages.append({"role": role, "content": content})

        # 最後再把最新的 user_text 加入
        messages.append({"role":"user","content":user_text})
        return messages# 回傳組好的 list，給 chat_client 使用

