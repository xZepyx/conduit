import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

from app.models.schemas import GenerateRequest
from app.providers.factory import get_provider, get_model_name


router = APIRouter()


@router.post("/api/generate")
async def generate(data: GenerateRequest):
    provider = get_provider(data.model)
    actual_model = get_model_name(data.model)

    messages = [{"role": "user", "content": data.prompt}]

    if not data.stream:
        try:
            content = await provider.chat(actual_model, messages)
            return JSONResponse({
                "model": data.model,
                "response": content,
                "done": True,
            })
        except Exception as e:
            return JSONResponse(
                {"error": str(e), "done": True},
                status_code=400,
            )

    async def event_stream():
        try:
            async for chunk in provider.stream_chat(actual_model, messages):
                if "error" in chunk:
                    yield json.dumps({"error": chunk["error"]}) + "\n"
                elif "done" in chunk:
                    yield json.dumps({"model": data.model, "response": "", "done": True}) + "\n"
                else:
                    yield json.dumps({
                        "model": data.model,
                        "response": chunk["content"],
                        "done": False,
                    }) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
            yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson",
    )
