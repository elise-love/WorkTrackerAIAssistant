"""
讀 .env、集中設定
"""
#config.py
from pathlib import Path # Pathlib 是 Python 3.4 之後的標準庫，提供了更方便的路徑操作
from dotenv import load_dotenv # python-dotenv 是一個用於讀取 .env 文件的庫, can read variables from .env file
import os 

"""
# 取得目前這個檔案（config.py）的絕對路徑，再往上一層得到專案根目錄
 __file__  → 目前檔案路徑
resolve()  → 轉成絕對路徑
parent     → 取得上一層資料夾
"""
ROOT = Path(__file__).resolve().parent

# 把專案根目錄再往上一層，找到 .env 檔（通常放在專案最外層）
# 之後將其中的變數載入到系統環境變數中
load_dotenv(ROOT/".."/".env")

# 讀取 .env 裡面的 OPENAI_API_KEY
# 如果 .env 沒有這個欄位，會得到 None
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

OPEN_ORG_ID = os.getenv("OPEN_ORG_ID","")
MODEL_DEFAULT = "gpt-4o"

# 設定 API 呼叫逾時秒數
TIMEOUT = 30