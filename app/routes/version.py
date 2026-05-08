from fastapi import APIRouter

router = APIRouter()

@router.get("/api/version")
async def version():
    return {
        "version": "0.5.7"
    }
