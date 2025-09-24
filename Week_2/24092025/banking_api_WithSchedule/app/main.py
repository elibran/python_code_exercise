from fastapi import FastAPI # type: ignore
from .routers.account_router import router as account_router
from .database import Base, engine
from .config import settings
from app.routers import scheduled_payment

app = FastAPI(title=settings.APP_NAME)
app.include_router(scheduled_payment.router, tags=["Scheduled Payments"])

@app.on_event("startup")
def on_startup():
    # Auto-create tables (for demo convenience)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"app": settings.APP_NAME, "message": "Welcome to the Personal Banking API"}

app.include_router(account_router)


# === API Versioning: minimal additive change ===
# New: mount the existing routers under /api/v1 while keeping backward-compatible routes.
from .api.v1 import router as v1_router
app.include_router(v1_router)