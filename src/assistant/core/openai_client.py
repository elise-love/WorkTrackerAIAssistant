"""
新增：跟 OpenAI API 溝通的薄封裝
① 讀取 API key（來自 config.py）
② 包裝 openai SDK 呼叫
③ 把錯誤轉成乾淨的 Python 例外	

你可以把它想成「負責打電話給 OpenAI 的小秘書」，具體職責：
使用 openai.ChatCompletion.create(...) 呼叫 OpenAI 的 Chat API。
管理 API 金鑰、組織 ID、timeout 等連線細節。
回傳最關鍵的 response.choices[0].message["content"] 給外部，省去 caller 解析 response 的麻煩。
完全不處理訊息內容，只管送出去、拿回來。
"""
# assistant/core/openai_client.py
import openai #import 官方sdk
from assistant.config import OPENAI_API_KEY, OPENAI_ORG_ID, TIMEOUT

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORG_ID


def chat_completion(messages, model, **opts):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            timeout=TIMEOUT,
            **opts,
            )
        return response.choices[0].message["content"]#只回傳最常用的 content 欄位，減少呼叫端解析負擔

    except openai.error.OPENAIError as exc: #所有 SDK 相關錯誤都繼承自 OpenAIError
        raise RuntimeError(f"OpenAI API error: {exc}") from exc



"""
 return response.choices[0].message["content"]:

    ChatCompletion 回傳長什麼樣？
         OpenAI 會回傳一個 巢狀 JSON（Python 裡是 OpenAIObject，用起來跟 dict / list 類似）：
            {
              "id": "chatcmpl‑abc123",
              "object": "chat.completion",
              "created": 1680000000,
              "model": "gpt-4o-mini",
              "choices": [
                {
                  "index": 0,
                  "message": {
                    "role": "assistant",
                    "content": "Here is the answer you asked for."
                  },
                  "finish_reason": "stop"
                }
              ],
              "usage": { … }
            }

     想拿到「模型回的文字」，要順著這條路徑走：
            response          # 最外層物件
            └─ ["choices"]    # list
               └─ [0]         # 第一個元素 (index 0)
                  └─ ["message"]   # dict
                     └─ ["content"] 
"""
