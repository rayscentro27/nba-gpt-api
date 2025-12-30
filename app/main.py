from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.db import engine
from app.models import Base
from app.api.router import router as api_router

# IMPORTANT: set this to your Render URL
PUBLIC_BASE_URL = "https://nba-gpt-api.onrender.com"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Render Postgres starts empty—create tables if missing
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="NBA GPT API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description="NBA stats API for Custom GPT Actions (FastAPI + Postgres cache)",
        routes=app.routes,
    )

    # Add the servers section required by GPT Actions
    schema["servers"] = [{"url": PUBLIC_BASE_URL}]

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi




