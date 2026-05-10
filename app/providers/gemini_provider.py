import json

import httpx

from app.config import GEMINI_API_KEY
from app.providers.base import BaseProvider


GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "gemini"

    async def stream_chat(self, model: str, messages: list):
        api_key = self._get_api_key()
        contents = self._convert_messages(messages)
        url = f"{GEMINI_BASE}/models/{model}:streamGenerateContent?key={api_key}&alt=sse"

        headers = {"Content-Type": "application/json"}
        payload = {"contents": contents}

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST", url, headers=headers, json=payload
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
                        candidates = parsed.get("candidates", [])
                        if not candidates:
                            continue
                        parts = candidates[0].get("content", {}).get("parts", [])
                        for part in parts:
                            text = part.get("text", "")
                            if text:
                                yield {"content": text}

                        finish = candidates[0].get("finishReason")
                        if finish and finish != "FINISH_REASON_UNSPECIFIED":
                            yield {"done": True}
                            return
                    except Exception:
                        continue

    async def chat(self, model: str, messages: list) -> str:
        api_key = self._get_api_key()
        contents = self._convert_messages(messages)
        url = f"{GEMINI_BASE}/models/{model}:generateContent?key={api_key}"

        headers = {"Content-Type": "application/json"}
        payload = {"contents": contents}

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                url, headers=headers, json=payload
            )
            return await self._parse_chat_response(response)

    def _convert_messages(self, messages):
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            gemini_role = "model" if role == "assistant" else "user"
            contents.append({
                "role": gemini_role,
                "parts": [{"text": content}],
            })
        return contents

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
            "error": f"Gemini error ({response.status_code}): {error_msg}"
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
                f"Gemini error ({response.status_code}): {error_msg}"
            )
        result = json.loads(text)
        candidates = result.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        return "".join(part.get("text", "") for part in parts)

    def _get_api_key(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        return GEMINI_API_KEY
