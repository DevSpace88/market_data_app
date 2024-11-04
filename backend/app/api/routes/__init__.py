# app/api/routes/__init__.py
from fastapi import APIRouter
from .auth import router as auth_router
from .market import router as market_router
from .websocket import router as websocket_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(market_router, prefix="/market", tags=["market"])
router.include_router(websocket_router, prefix="/ws", tags=["websocket"])