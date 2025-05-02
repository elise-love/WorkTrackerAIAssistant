"""
新增：跟 OpenAI API 溝通的薄封裝
① 讀取 API key（來自 config.py）
② 包裝 openai SDK 呼叫
③ 把錯誤轉成乾淨的 Python 例外	

不組 prompt、不存歷史
"""