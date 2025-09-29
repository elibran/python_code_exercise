from fastapi import APIRouter # type: ignore
from .routes import practitioners, slots

router = APIRouter()
router.include_router(practitioners.router, prefix="/practitioners", tags=["practitioners"]) 
router.include_router(slots.router, prefix="/slots", tags=["slots"]) 
