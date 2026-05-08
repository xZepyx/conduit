import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.providers.openrouter import stream_chat_completion

router = APIRouter()

async def handle_chat(request: Request):
    body = await request.json()

    model = body.get("model", "llama3")
    messages = body.get("messages", [])

    async def event_stream():
        async for chunk in stream_chat_completion(model, messages):

            data = {
                "id": "chatcmpl-1",
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "delta": {
                            "content": chunk
                        },
                        "index": 0,
                        "finish_reason": None
                    }
                ]
            }

            yield f"data: {json.dumps(data)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )

@router.post("/v1/chat/completions")
async def v1_chat(request: Request):
    return await handle_chat(request)

@router.post("/chat/completions")
async def chat(request: Request):
    return await handle_chat(request)
