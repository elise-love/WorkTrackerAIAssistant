# assistant/core/openai_client.py
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_ORG_ID, TIMEOUT

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


if __name__ =='__main__':
    chat_completion()

