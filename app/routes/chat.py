import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.providers.factory import get_provider, get_model_name


router = APIRouter()


@router.post("/api/chat")
async def chat(data: ChatRequest):
    provider = get_provider(data.model)
    actual_model = get_model_name(data.model)

    async def event_stream():
        try:
            async for chunk in provider.stream_chat(actual_model, data.messages):
                if "error" in chunk:
                    yield json.dumps({"error": chunk["error"]}) + "\n"
                elif "done" in chunk:
                    yield json.dumps({"model": data.model, "message": {"role": "assistant", "content": ""}, "done": True}) + "\n"
                else:
                    yield json.dumps({
                        "model": data.model,
                        "message": {"role": "assistant", "content": chunk["content"]},
                        "done": False,
                    }) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
            yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson",
    )
