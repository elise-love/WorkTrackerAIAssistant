from openai import OpenAI
client = OpenAI()

def chat_completion(messages: list[dict], model: str, prompt_id: str = None) -> str:
    kwargs = {
        "model": model,
        "messages": messages,
    }
    if prompt_id:
        kwargs["prompt_id"] = prompt_id

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content
