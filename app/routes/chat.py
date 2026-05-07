from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.providers.openrouter import stream_chat_completion


router = APIRouter()


@router.post("/api/chat")
async def chat(data: ChatRequest):

    generator = stream_chat_completion(
        model=data.model,
        messages=data.messages
    )

    return StreamingResponse(
        generator,
        media_type="application/x-ndjson"
    )