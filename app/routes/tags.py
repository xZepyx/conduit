from fastapi import APIRouter


router = APIRouter()


@router.get("/api/tags")
async def tags():

    return {
        "models": [
            {
                "name": "llama3"
            },
            {
                "name": "deepseek"
            },
            {
                "name": "gpt4"
            }
        ]
    }