from fastapi import APIRouter
from app.db.session import db_ping
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    ok = db_ping()
    logger.info("Health check - db=%s", "ok" if ok else "degraded")
    return {"status": "ok" if ok else "degraded"}
