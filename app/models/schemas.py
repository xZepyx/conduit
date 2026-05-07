from pydantic import BaseModel
from typing import List, Dict, Any


class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    stream: bool = True