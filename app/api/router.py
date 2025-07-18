from fastapi import APIRouter
from .endpoints import upload, items, search, websocket

router = APIRouter()
router.include_router(upload.router, prefix="/upload", tags=["upload"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(websocket.router)