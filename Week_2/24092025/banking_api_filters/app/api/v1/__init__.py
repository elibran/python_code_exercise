# FastAPI API v1 router aggregator
from fastapi import APIRouter # type: ignore
# Import existing routers and mount them under /api/v1 without modifying their original files
from ...routers.account_router import router as account_router

router = APIRouter(prefix="/api/v1")

# Reuse existing functionality as-is
router.include_router(account_router)
