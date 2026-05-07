import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from app.providers.openrouter import stream_chat_completion
from app.providers.openrouter import chat_completion


router = APIRouter()


@router.post("/api/generate")
async def generate(data: dict):

    prompt = data.get("prompt", "")
    model = data.get("model", "llama3")
    stream = data.get("stream", False)

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    # NON-STREAM MODE
    if not stream:

        result = await chat_completion(
            model=model,
            messages=messages
        )

        content = result["choices"][0]["message"]["content"]

        return JSONResponse({
            "model": model,
            "response": content,
            "done": True
        })

    # STREAM MODE
    async def generator():

        async for chunk in stream_chat_completion(model, messages):

            parsed = json.loads(chunk)

            if parsed.get("done"):

                yield json.dumps({
                    "model": model,
                    "response": "",
                    "done": True
                }) + "\n"

                continue

            content = (
                parsed.get("message", {})
                .get("content", "")
            )

            yield json.dumps({
                "model": model,
                "response": content,
                "done": False
            }) + "\n"

    return StreamingResponse(
        generator(),
        media_type="application/x-ndjson"
    )