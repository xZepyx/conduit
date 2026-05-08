from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/api/show")
async def show(request: Request):
    body = await request.json()

    return {
        "license": "",
        "modelfile": "",
        "parameters": "",
        "template": "",
        "details": {
            "family": "llama",
            "format": "gguf",
            "parameter_size": "70B",
            "quantization_level": "Q4_K_M"
        }
    }
