# backend/app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import asyncio

from ..models.database import get_db
from ..services.market_service import MarketService
from ..services.ai_analysis_service import MarketAIAnalysis
from ..services.websocket_manager import WebSocketManager

router = APIRouter()
ws_manager = WebSocketManager()


@router.get("/market/data/{symbol}")
async def get_market_data(
        symbol: str,
        timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
        db: Session = Depends(get_db)
):
    """
    Fetch market data for a specific symbol

    - **symbol**: Stock symbol (e.g., AAPL, GOOGL)
    - **timeframe**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
    """
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol, timeframe)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/market/analysis/{symbol}")
async def get_market_analysis(
        symbol: str,
        include_news: bool = Query(True, description="Include news analysis"),
        db: Session = Depends(get_db)
):
    """
    Get comprehensive market analysis including technical indicators and AI insights

    - **symbol**: Stock symbol
    - **include_news**: Whether to include news analysis
    """
    try:
        # Initialize services
        market_service = MarketService(db)
        ai_service = MarketAIAnalysis()

        # Fetch market data
        market_data = await market_service.fetch_market_data(symbol)
        if not market_data:
            raise HTTPException(
                status_code=404,
                detail=f"Market data not found for symbol {symbol}"
            )

        # Calculate indicators
        technical_data = market_service.calculate_technical_indicators(market_data)

        # Detect patterns
        patterns = await market_service.detect_patterns(market_data)

        # Generate signals
        signals = market_service.generate_signals(market_data, technical_data)

        # Get AI analysis
        ai_analysis = await ai_service.generate_market_summary(
            symbol=symbol,
            market_data=market_data,
            technical_data=technical_data,
            patterns=patterns
        )

        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_data": market_data[-100:],  # Last 100 data points
            "technical_indicators": technical_data,
            "patterns": patterns,
            "signals": signals,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing market data: {str(e)}"
        )


@router.get("/market/indicators/{symbol}")
async def get_technical_indicators(
        symbol: str,
        indicators: Optional[List[str]] = Query(None),
        db: Session = Depends(get_db)
):
    """
    Get specific technical indicators for a symbol

    - **symbol**: Stock symbol
    - **indicators**: List of requested indicators (e.g., RSI, MACD, SMA)
    """
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    technical_data = market_service.calculate_technical_indicators(data)

    if indicators:
        return {
            "symbol": symbol,
            "indicators": {k: v for k, v in technical_data.items() if k in indicators}
        }

    return {
        "symbol": symbol,
        "indicators": technical_data
    }


@router.get("/market/patterns/{symbol}")
async def get_market_patterns(
        symbol: str,
        db: Session = Depends(get_db)
):
    """Get detected patterns for a symbol"""
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    patterns = await market_service.detect_patterns(data)
    return {
        "symbol": symbol,
        "patterns": patterns
    }


@router.get("/market/signals/{symbol}")
async def get_trading_signals(
        symbol: str,
        db: Session = Depends(get_db)
):
    """Get trading signals for a symbol"""
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    technical_data = market_service.calculate_technical_indicators(data)
    signals = market_service.generate_signals(data, technical_data)

    return {
        "symbol": symbol,
        "signals": signals
    }


@router.get("/market/watchlist")
async def get_watchlist_data(
        symbols: List[str] = Query(...),
        db: Session = Depends(get_db)
):
    """
    Get market data for multiple symbols simultaneously

    - **symbols**: List of stock symbols
    """
    market_service = MarketService(db)
    results = {}

    for symbol in symbols:
        try:
            data = await market_service.fetch_market_data(symbol)
            if data:
                technical_data = market_service.calculate_technical_indicators(data)
                results[symbol] = {
                    "market_data": data[-1],  # Latest data point
                    "technical_indicators": technical_data
                }
        except Exception as e:
            results[symbol] = {"error": str(e)}

    return results


@router.websocket("/ws/market/{symbol}")
async def websocket_endpoint(
        websocket: WebSocket,
        symbol: str,
        db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time market updates"""
    try:
        await ws_manager.connect(websocket, symbol)

        while True:
            try:
                # Check for client messages (e.g., change timeframe)
                data = await websocket.receive_json()
                if data.get('type') == 'subscribe':
                    # Handle subscription changes
                    pass

            except WebSocketDisconnect:
                break

            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    finally:
        await ws_manager.disconnect(websocket, symbol)


# Error Handlers
@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }


@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "Internal server error",
        "detail": str(exc),
        "status_code": 500,
        "timestamp": datetime.now().isoformat()
    }