# from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query, WebSocketDisconnect
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from datetime import datetime
# import logging
# import json
#
# from ..models.database import get_db
# from ..services.market_service import MarketService
# from ..services.ai_analysis_service import MarketAIAnalysis
# from ..services.websocket_manager import WebSocketManager
#
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
#
# router = APIRouter()
# ws_manager = WebSocketManager()
#
# # Initialize AI Analysis with debug mode
# market_ai = MarketAIAnalysis()
# market_ai.set_debug(True)  # Hier wird der Debug-Modus aktiviert
#
# @router.get("/market/data/{symbol}")
# async def get_market_data(
#         symbol: str,
#         timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
#         db: Session = Depends(get_db)
# ):
#     """Fetch market data for a specific symbol"""
#     logger.debug(f"Fetching market data for symbol: {symbol}, timeframe: {timeframe}")
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol, timeframe)
#
#     if not data:
#         logger.error(f"No data found for symbol {symbol}")
#         raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#     return {
#         "symbol": symbol,
#         "timeframe": timeframe,
#         "data": data,
#         "timestamp": datetime.now().isoformat()
#     }
#
# @router.get("/market/analysis/{symbol}")
# async def get_market_analysis(
#         symbol: str,
#         timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
#         include_news: bool = Query(True),
#         db: Session = Depends(get_db)
# ):
#     """Get comprehensive market analysis"""
#     try:
#         market_service = MarketService(db)
#
#         # Verwende die bereits initialisierte AI-Service-Instanz mit Debug
#         timeframe_map = {
#             "1D": ("1d", "5m"),
#             "1W": ("7d", "1h"),
#             "1M": ("1mo", "1d"),
#             "3M": ("3mo", "1d"),
#             "6M": ("6mo", "1d"),
#             "1Y": ("1y", "1d"),
#             "YTD": ("ytd", "1d")
#         }
#         period, interval = timeframe_map.get(timeframe, ("1mo", "1h"))
#
#         market_data = await market_service.fetch_market_data(symbol, period=period, interval=interval)
#         if not market_data:
#             raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#         technical_data = market_service.calculate_technical_indicators(market_data)
#         patterns = await market_service.detect_patterns(market_data)
#         signals = market_service.generate_signals(market_data, technical_data)
#
#         # Verwende die globale market_ai Instanz
#         ai_analysis = await market_ai.generate_market_summary(
#             symbol=symbol,
#             market_data=market_data,
#             technical_data=technical_data,
#             patterns=patterns
#         )
#
#         return {
#             "symbol": symbol,
#             "timestamp": datetime.now().isoformat(),
#             "market_data": market_data,
#             "technical_indicators": technical_data,
#             "patterns": patterns,
#             "signals": signals,
#             "ai_analysis": ai_analysis,
#             "timeframe": timeframe
#         }
#
#     except Exception as e:
#         logger.error(f"Error in market analysis: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Error analyzing market data: {str(e)}")
#
#
# @router.get("/market/indicators/{symbol}")
# async def get_technical_indicators(
#         symbol: str,
#         indicators: Optional[List[str]] = Query(None),
#         db: Session = Depends(get_db)
# ):
#     """Get specific technical indicators for a symbol"""
#     logger.debug(f"Fetching technical indicators for {symbol}")
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         logger.error(f"No market data found for symbol {symbol}")
#         raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#     technical_data = market_service.calculate_technical_indicators(data)
#
#     if indicators:
#         return {
#             "symbol": symbol,
#             "indicators": {k: v for k, v in technical_data.items() if k in indicators}
#         }
#
#     return {
#         "symbol": symbol,
#         "indicators": technical_data
#     }
#
#
# @router.get("/market/patterns/{symbol}")
# async def get_market_patterns(
#         symbol: str,
#         db: Session = Depends(get_db)
# ):
#     """Get detected patterns for a symbol"""
#     logger.debug(f"Detecting patterns for {symbol}")
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#     patterns = await market_service.detect_patterns(data)
#     return {
#         "symbol": symbol,
#         "patterns": patterns
#     }
#
#
# @router.get("/market/signals/{symbol}")
# async def get_trading_signals(
#         symbol: str,
#         db: Session = Depends(get_db)
# ):
#     """Get trading signals for a symbol"""
#     logger.debug(f"Generating trading signals for {symbol}")
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#     technical_data = market_service.calculate_technical_indicators(data)
#     signals = market_service.generate_signals(data, technical_data)
#
#     return {
#         "symbol": symbol,
#         "signals": signals
#     }
#
#
# @router.get("/market/watchlist")
# async def get_watchlist_data(
#         symbols: List[str] = Query(...),
#         db: Session = Depends(get_db)
# ):
#     """Get market data for multiple symbols simultaneously"""
#     logger.debug(f"Processing watchlist data for symbols: {symbols}")
#     market_service = MarketService(db)
#     results = {}
#
#     for symbol in symbols:
#         try:
#             data = await market_service.fetch_market_data(symbol)
#             if data:
#                 technical_data = market_service.calculate_technical_indicators(data)
#                 results[symbol] = {
#                     "market_data": data[-1],
#                     "technical_indicators": technical_data
#                 }
#         except Exception as e:
#             results[symbol] = {"error": str(e)}
#
#     return results
#
#
# @router.websocket("/ws/market/{symbol}")
# async def websocket_endpoint(
#         websocket: WebSocket,
#         symbol: str,
#         db: Session = Depends(get_db)
# ):
#     """WebSocket endpoint for real-time market updates"""
#     connection_id = f"{symbol}_{datetime.now().timestamp()}"
#
#     try:
#         await ws_manager.connect(websocket, symbol)
#
#         while True:
#             try:
#                 data = await websocket.receive_json()
#                 message_type = data.get('type')
#
#                 if message_type == 'subscribe':
#                     await ws_manager.handle_subscription_change(websocket, data)
#                 elif message_type == 'timeframe_change':
#                     pass  # Handle timeframe changes
#                 elif message_type == 'ping':
#                     await websocket.send_json({"type": "pong"})
#
#             except WebSocketDisconnect:
#                 break
#             except Exception as e:
#                 logger.error(f"WebSocket error: {str(e)}")
#                 try:
#                     await websocket.send_json({
#                         "type": "error",
#                         "message": "Internal server error"
#                     })
#                 except:
#                     break
#     finally:
#         await ws_manager.disconnect(websocket, symbol)


# app/api/routes.py
from fastapi import APIRouter
from .routes.auth import router as auth_router
from .routes.market import router as market_router
from .routes.admin import router as admin_router
from .routes.websocket import router as websocket_router
from .routes.watchlist import router as watchlist_router
from .routes.ai_settings import router as ai_settings_router

router = APIRouter()

# Registriere die Routen mit korrekten Präfixen
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(market_router, prefix="/market", tags=["market"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(websocket_router, prefix="/ws", tags=["websocket"])
router.include_router(watchlist_router, prefix="/watchlist", tags=["watchlist"])
router.include_router(ai_settings_router, prefix="/ai-settings", tags=["ai-settings"])