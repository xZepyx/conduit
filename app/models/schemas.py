from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    stream: bool = True


class GenerateRequest(BaseModel):
    model: str = "llama3"
    prompt: str = ""
    stream: bool = False
    options: Optional[Dict[str, Any]] = None
