from fastapi import APIRouter, Request

from app.providers.factory import get_model_info


router = APIRouter()


@router.post("/api/show")
async def show(request: Request):
    body = await request.json()
    model = body.get("model", "llama3")
    return get_model_info(model)
