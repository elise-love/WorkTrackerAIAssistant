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
from openai import OpenAI
from assistant.config import OPENAI_API_KEY, OPENAI_ORG_ID, TIMEOUT

client = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORG_ID,
    timeout=TIMEOUT
)


def chat_completion(messages, model, **opts):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **opts,
        )
        return response.choices[0].message.content
    except Exception as exc:
        raise RuntimeError(f"OpenAI API error: {exc}") from exc



