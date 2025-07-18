#chat_client
from core.openai_client import run_assistant

def send(user_text: str, history: list[tuple[str, str]], profile_id: str = "Elfie") -> str:
    assistant_text = run_assistant(user_text)
    history.append((user_text, assistant_text))
    return assistant_text

if __name__ == "__main__":
    history: list[tuple[str, str]] = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = send(user_input, history)
        print("Elfie:", response)