"""
config.py —— 讀取 .env 與集中設定

1. 透過 python‑dotenv 自動載入最外層 `.env`
2. 把必要的環境變數拉成全域常數
3. 若缺少必要變數，提早丟錯避免執行期才炸
"""

from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise ImportError("請先執行 `pip install python-dotenv`") from e

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

def _need(name: str) -> str:
    """沒有就直接 raise ValueError，讓錯誤在一開始就顯示"""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"環境變數 {name} 尚未設定，請在 .env 加上它。")
    return value

OPENAI_API_KEY = _need("OPENAI_API_KEY")


OPENAI_ORG_ID  = os.getenv("OPENAI_ORG_ID", "")

MODEL_DEFAULT  = os.getenv("MODEL_DEFAULT", "gpt-4.1")


TIMEOUT        = int(os.getenv("OPENAI_TIMEOUT", "30"))

ASSISTANT_ID = os.getenv("ASSISTANT_ID", "")

THREAD_ID = "thread_eLXbn0XwAhf82Sf8JjwVpLF6"
