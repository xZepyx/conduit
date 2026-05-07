from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.tags import router as tags_router
from app.routes.generate import router as generate_router


app = FastAPI(title="Conduit")


app.include_router(chat_router)
app.include_router(tags_router)
app.include_router(generate_router)