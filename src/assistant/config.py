"""
config.py —— 讀取 .env 與集中設定

1. 透過 python‑dotenv 自動載入最外層 `.env`
2. 把必要的環境變數拉成全域常數
3. 若缺少必要變數，提早丟錯避免執行期才炸
"""

from pathlib import Path
import os

# ----------------------------------------
# 1. 自動載入 .env
# ----------------------------------------
try:
    from dotenv import load_dotenv
except ImportError as e:  # 還沒安裝 python-dotenv
    raise ImportError("請先執行 `pip install python-dotenv`") from e

# 這支檔案位於 src/assistant/config.py
# 專案根目錄通常是 src 的上一層，再往上一層才是 repo 最外層
BASE_DIR = Path(__file__).resolve().parents[2]   # WorkTrackerAIAssistant/
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)  # 沒找到 .env 也不會報錯；找到了就載

# ----------------------------------------
# 2. 讀環境變數 → 全域常數
# ----------------------------------------
def _need(name: str) -> str:
    """沒有就直接 raise ValueError，讓錯誤在一開始就顯示"""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"環境變數 {name} 尚未設定，請在 .env 加上它。")
    return value

OPENAI_API_KEY = _need("OPENAI_API_KEY")

# 用 os.getenv，沒設定給空字串
OPENAI_ORG_ID  = os.getenv("OPENAI_ORG_ID", "")

MODEL_DEFAULT  = os.getenv("MODEL_DEFAULT", "gpt-4.1")

# API 逾時秒數；可自行在 .env 覆寫
TIMEOUT        = int(os.getenv("OPENAI_TIMEOUT", "30"))

SYSTEM_PROMPT = (
    "You are Elfie, my personal assistant. "
    )
