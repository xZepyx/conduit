import json

import httpx

from app.providers.base import BaseProvider


_API_KEY_SOURCES = {}


def _get_key_source(env_name):
    from app import config
    return getattr(config, env_name, None)


class OpenAIProvider(BaseProvider):

    provider_name = "openai"
    api_key_env = "OPENAI_API_KEY"
    base_url = "https://api.openai.com/v1/chat/completions"

    @property
    def name(self) -> str:
        return self.provider_name

    async def stream_chat(self, model: str, messages: list):
        api_key = self._get_api_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "stream_options": {"include_usage": False},
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST", self.base_url, headers=headers, json=payload
            ) as response:
                if response.status_code != 200:
                    async for item in self._handle_error(response):
                        yield item
                    return

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data = line.removeprefix("data: ")
                    if data == "[DONE]":
                        yield {"done": True}
                        return
                    try:
                        parsed = json.loads(data)
                        delta = parsed["choices"][0]["delta"]
                        content = delta.get("content")
                        if content:
                            yield {"content": content}
                    except Exception:
                        continue

    async def chat(self, model: str, messages: list) -> str:
        api_key = self._get_api_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages}

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                self.base_url, headers=headers, json=payload
            )
            return await self._parse_chat_response(response)

    async def _handle_error(self, response):
        text = await response.aread()
        try:
            error_data = json.loads(text)
            error_msg = error_data.get("error", {}).get(
                "message", text.decode()
            )
        except Exception:
            error_msg = text.decode()
        yield {
            "error": f"{self.provider_name.capitalize()} error ({response.status_code}): {error_msg}"
        }
        yield {"done": True}

    async def _parse_chat_response(self, response):
        text = await response.aread()
        if response.status_code != 200:
            try:
                error_data = json.loads(text)
                error_msg = error_data.get("error", {}).get(
                    "message", text.decode()
                )
            except Exception:
                error_msg = text.decode()
            raise Exception(
                f"{self.provider_name.capitalize()} error ({response.status_code}): {error_msg}"
            )
        result = json.loads(text)
        return result["choices"][0]["message"]["content"]

    def _get_api_key(self):
        key = _get_key_source(self.api_key_env)
        if not key:
            raise ValueError(
                f"{self.api_key_env} is not set. Add it to your .env file."
            )
        return key
