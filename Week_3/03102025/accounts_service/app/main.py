from fastapi import FastAPI # type: ignore
from app.core.config import get_settings
from app.core.logging import configure_logging, request_logger_middleware
from app.db.models import Base
from app.db.session import engine
from app.api.accounts import router as accounts_router
from app.api.reference import router as reference_router
from app.api.health import router as health_router

settings = get_settings()
configure_logging(settings.log_level)

# Create tables at startup (demo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Accounts Mini-Service", version="1.0.0")
app.middleware("http")(request_logger_middleware)

app.include_router(accounts_router)
app.include_router(reference_router)
app.include_router(health_router)
