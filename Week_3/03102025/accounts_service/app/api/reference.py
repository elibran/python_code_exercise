from functools import lru_cache
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["reference"])

@lru_cache(maxsize=1)
def _account_types() -> list[str]:
    logger.debug("Using cached account types")
    return ["SAVINGS", "CURRENT", "BROKERAGE"]

@router.get("/reference/account-types", response_model=list[str])
def get_account_types():
    logger.info("GET /reference/account-types")
    return _account_types()
