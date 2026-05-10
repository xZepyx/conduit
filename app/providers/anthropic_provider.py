import json

import httpx

from app.config import ANTHROPIC_API_KEY
from app.providers.base import BaseProvider


ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


class AnthropicProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "anthropic"

    async def stream_chat(self, model: str, messages: list):
        api_key = self._get_api_key()
        system, converted = self._convert_messages(messages)

        headers = {
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": converted,
            "max_tokens": 4096,
            "stream": True,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST", ANTHROPIC_URL, headers=headers, json=payload
            ) as response:
                if response.status_code != 200:
                    async for item in self._handle_error(response):
                        yield item
                    return

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data = line.removeprefix("data: ")
                    try:
                        parsed = json.loads(data)
                        event_type = parsed.get("type")

                        if event_type == "content_block_delta":
                            delta = parsed.get("delta", {})
                            if delta.get("type") == "text_delta":
                                text = delta.get("text", "")
                                if text:
                                    yield {"content": text}

                        elif event_type == "message_stop":
                            yield {"done": True}
                            return

                    except Exception:
                        continue

    async def chat(self, model: str, messages: list) -> str:
        api_key = self._get_api_key()
        system, converted = self._convert_messages(messages)

        headers = {
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": converted,
            "max_tokens": 4096,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                ANTHROPIC_URL, headers=headers, json=payload
            )
            return await self._parse_chat_response(response)

    def _convert_messages(self, messages):
        system = None
        converted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                system = content
            else:
                anthropic_role = "assistant" if role == "assistant" else "user"
                converted.append({
                    "role": anthropic_role,
                    "content": content,
                })
        return system, converted

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
            "error": f"Anthropic error ({response.status_code}): {error_msg}"
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
                f"Anthropic error ({response.status_code}): {error_msg}"
            )
        result = json.loads(text)
        content_blocks = result.get("content", [])
        return "".join(
            block.get("text", "")
            for block in content_blocks
            if block.get("type") == "text"
        )

    def _get_api_key(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file."
            )
        return ANTHROPIC_API_KEY
