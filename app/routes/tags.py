from fastapi import APIRouter

from app.providers.factory import get_all_models


router = APIRouter()


@router.get("/api/tags")
async def tags():
    return {
        "models": [{"name": name} for name in get_all_models()],
    }
