from contextlib import asynccontextmanager
from fastapi import FastAPI # type: ignore
from app.api.v1.error_handlers import init_error_handlers
from app.api.v1.api_router import router as api_v1_router
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Clinic Slots API", version="1.0.0", lifespan=lifespan)
init_error_handlers(app)
app.include_router(api_v1_router, prefix="/api/v1")
