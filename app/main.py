from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.tags import router as tags_router
from app.routes.generate import router as generate_router
from app.routes.version import router as version_router
from app.routes.show import router as show_router
from app.routes.openai import router as openai_router

app = FastAPI(title="Conduit")


app.include_router(chat_router)
app.include_router(tags_router)
app.include_router(generate_router)
app.include_router(version_router)
app.include_router(show_router)
app.include_router(openai_router)
