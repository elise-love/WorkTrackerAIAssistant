# assistant/__main__.py
import readline # 命令列編輯體驗更好，提升命令列編輯體驗：方向鍵可切換歷史、Emacs 快捷鍵等
from assistant.core.chat_client import send

def main() -> None:
    history: list[tuple[str,str]]=[]
    print("🔹 Chat CLI，離開請輸入 /quit")# 儲存對話歷史，格式 (speaker, text)
   
    while True:# 不斷等待使用者輸入，直到明確離開
        try: 
            user_text = input("You: ").strip() # 讀取並去除前後空白
        except(EOFError, KeyboardInterrupt): # Ctrl‑D 或 Ctrl‑C
            print("\nBye!")

            break
        # 若使用者輸入離開指令，結束程式
        if user_text.lower() in {"/quit", "exit"}:
            print("Bye!")
            break

        if not user_text:
            continue

        # 把使用者輸入存進對話歷史
        history.append(("user", user_text))

        # 呼叫 send() 取得模型回覆，並帶入完整歷史做上下文
        reply = send(user_text,history)

        # 把回覆也存進歷史，讓下一輪有上下文
        history.append(("assistant", reply))

        print(f"Elfie:{reply}\n")

if __name__ =="__main__":
    main()

"""
$env:PYTHONPATH = "src"
python -m assistant
"""