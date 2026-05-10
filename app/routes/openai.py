import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.providers.factory import get_provider, get_model_name


router = APIRouter()


async def handle_chat(request: Request):
    body = await request.json()
    model = body.get("model", "llama3")
    messages = body.get("messages", [])

    provider = get_provider(model)
    actual_model = get_model_name(model)

    async def event_stream():
        try:
            async for chunk in provider.stream_chat(actual_model, messages):
                if "error" in chunk:
                    data = {"error": {"message": chunk["error"]}}
                    yield f"data: {json.dumps(data)}\n\n"
                    yield "data: [DONE]\n\n"
                    return
                elif "done" in chunk:
                    yield "data: [DONE]\n\n"
                    return
                else:
                    data = {
                        "id": "chatcmpl-1",
                        "object": "chat.completion.chunk",
                        "choices": [
                            {
                                "delta": {"content": chunk["content"]},
                                "index": 0,
                            }
                        ],
                    }
                    yield f"data: {json.dumps(data)}\n\n"
        except Exception as e:
            data = {"error": {"message": str(e)}}
            yield f"data: {json.dumps(data)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


@router.post("/v1/chat/completions")
async def v1_chat(request: Request):
    return await handle_chat(request)


@router.post("/chat/completions")
async def chat(request: Request):
    return await handle_chat(request)
