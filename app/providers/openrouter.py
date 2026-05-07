import json

import httpx

from app.config import OPENROUTER_API_KEY


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


MODEL_MAP = {
    "llama3": "meta-llama/llama-3.3-70b-instruct",
    "deepseek": "deepseek/deepseek-chat",
    "gpt4": "openai/gpt-4.1"
}


async def stream_chat_completion(model: str, messages: list):

    mapped_model = MODEL_MAP.get(
        model,
        "meta-llama/llama-3.3-70b-instruct"
    )
    payload = {
        "model": mapped_model,
        "messages": messages,
        "stream": True
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=None) as client:

        async with client.stream(
            "POST",
            OPENROUTER_URL,
            headers=headers,
            json=payload
        ) as response:

            if response.status_code != 200:

                text = await response.aread()

                print(text.decode())

                raise Exception(
                    f"OpenRouter error: {response.status_code}"
                )

            async for line in response.aiter_lines():

                if not line:
                    continue

                if not line.startswith("data: "):
                    continue

                data = line.removeprefix("data: ")

                if data == "[DONE]":

                    final_chunk = {
                        "done": True
                    }

                    yield json.dumps(final_chunk) + "\n"
                    break

                try:
                    parsed = json.loads(data)

                    delta = parsed["choices"][0]["delta"]

                    content = delta.get("content")

                    if not content:
                        continue

                    ollama_chunk = {
                        "model": model,
                        "message": {
                            "role": "assistant",
                            "content": content
                        },
                        "done": False
                    }

                    yield json.dumps(ollama_chunk) + "\n"

                except Exception:
                    continue

async def chat_completion(model: str, messages: list):

    mapped_model = MODEL_MAP.get(
        model,
        "meta-llama/llama-3.3-70b-instruct"
    )

    payload = {
        "model": mapped_model,
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=120) as client:

        response = await client.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload
        )

        text = await response.aread()

        if response.status_code != 200:
            print(text.decode())
            raise Exception("OpenRouter error")

        return json.loads(text)