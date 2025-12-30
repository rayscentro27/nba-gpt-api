from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import engine
from app.models import Base
from app.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Render Postgres starts empty—create tables if missing
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="NBA GPT API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)



