# from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query, WebSocketDisconnect
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from datetime import datetime
#
# from ..models.database import get_db
# from ..services.market_service import MarketService
# from ..services.ai_analysis_service import MarketAIAnalysis
# from ..services.websocket_manager import WebSocketManager
#
# router = APIRouter()
# ws_manager = WebSocketManager()
#
#
# @router.get("/market/data/{symbol}")
# async def get_market_data(
#         symbol: str,
#         timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
#         db: Session = Depends(get_db)
# ):
#     """
#     Fetch market data for a specific symbol
#     """
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol, timeframe)
#
#     if not data:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Market data not found for symbol {symbol}"
#         )
#
#     return {
#         "symbol": symbol,
#         "timeframe": timeframe,
#         "data": data,
#         "timestamp": datetime.now().isoformat()
#     }
#
#
# @router.get("/market/analysis/{symbol}")
# async def get_market_analysis(
#         symbol: str,
#         include_news: bool = Query(True, description="Include news analysis"),
#         db: Session = Depends(get_db)
# ):
#     """
#     Get comprehensive market analysis
#     """
#     try:
#         market_service = MarketService(db)
#         ai_service = MarketAIAnalysis()
#
#         market_data = await market_service.fetch_market_data(symbol)
#         if not market_data:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Market data not found for symbol {symbol}"
#             )
#
#         technical_data = market_service.calculate_technical_indicators(market_data)
#         patterns = await market_service.detect_patterns(market_data)
#         signals = market_service.generate_signals(market_data, technical_data)
#
#         ai_analysis = await ai_service.generate_market_summary(
#             symbol=symbol,
#             market_data=market_data,
#             technical_data=technical_data,
#             patterns=patterns
#         )
#
#         return {
#             "symbol": symbol,
#             "timestamp": datetime.now().isoformat(),
#             "market_data": market_data[-100:],
#             "technical_indicators": technical_data,
#             "patterns": patterns,
#             "signals": signals,
#             "ai_analysis": ai_analysis
#         }
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error analyzing market data: {str(e)}"
#         )
#
# @router.get("/market/indicators/{symbol}")
# async def get_technical_indicators(
#         symbol: str,
#         indicators: Optional[List[str]] = Query(None),
#         db: Session = Depends(get_db)
# ):
#     """
#     Get specific technical indicators for a symbol
#
#     - **symbol**: Stock symbol
#     - **indicators**: List of requested indicators (e.g., RSI, MACD, SMA)
#     """
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Market data not found for symbol {symbol}"
#         )
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
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Market data not found for symbol {symbol}"
#         )
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
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol)
#
#     if not data:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Market data not found for symbol {symbol}"
#         )
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
#     """
#     Get market data for multiple symbols simultaneously
#
#     - **symbols**: List of stock symbols
#     """
#     market_service = MarketService(db)
#     results = {}
#
#     for symbol in symbols:
#         try:
#             data = await market_service.fetch_market_data(symbol)
#             if data:
#                 technical_data = market_service.calculate_technical_indicators(data)
#                 results[symbol] = {
#                     "market_data": data[-1],  # Latest data point
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
#     try:
#         await ws_manager.connect(websocket, symbol)
#         while True:
#             try:
#                 # Check for client messages
#                 data = await websocket.receive_json()
#                 if data.get('type') == 'subscribe':
#                     # Handle subscription changes
#                     pass
#
#             except WebSocketDisconnect:
#                 break
#             except Exception as e:
#                 print(f"WebSocket error: {e}")
#                 break
#
#     finally:
#         await ws_manager.disconnect(websocket, symbol)


from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

# Logging Setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    """
    logger.debug(f"Fetching market data for symbol: {symbol}, timeframe: {timeframe}")
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol, timeframe)

    if not data:
        logger.error(f"No data found for symbol {symbol}")
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    logger.debug(f"Successfully fetched {len(data)} data points for {symbol}")
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
    Get comprehensive market analysis
    """
    logger.debug(f"Starting comprehensive analysis for symbol: {symbol}")
    try:
        market_service = MarketService(db)
        ai_service = MarketAIAnalysis()

        logger.debug(f"Fetching market data for {symbol}")
        market_data = await market_service.fetch_market_data(symbol)
        if not market_data:
            logger.error(f"No market data found for symbol {symbol}")
            raise HTTPException(
                status_code=404,
                detail=f"Market data not found for symbol {symbol}"
            )

        logger.debug("Calculating technical indicators")
        technical_data = market_service.calculate_technical_indicators(market_data)

        logger.debug("Detecting patterns")
        patterns = await market_service.detect_patterns(market_data)

        logger.debug("Generating trading signals")
        signals = market_service.generate_signals(market_data, technical_data)

        logger.debug("Generating AI analysis")
        ai_analysis = await ai_service.generate_market_summary(
            symbol=symbol,
            market_data=market_data,
            technical_data=technical_data,
            patterns=patterns
        )

        logger.debug("Analysis completed successfully")
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_data": market_data[-100:],
            "technical_indicators": technical_data,
            "patterns": patterns,
            "signals": signals,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        logger.error(f"Error during market analysis: {str(e)}", exc_info=True)
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
    """
    logger.debug(f"Fetching technical indicators for {symbol}")
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        logger.error(f"No market data found for symbol {symbol}")
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    logger.debug("Calculating technical indicators")
    technical_data = market_service.calculate_technical_indicators(data)

    if indicators:
        logger.debug(f"Filtering for specific indicators: {indicators}")
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
    logger.debug(f"Detecting patterns for {symbol}")
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        logger.error(f"No market data found for symbol {symbol}")
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    patterns = await market_service.detect_patterns(data)
    logger.debug(f"Found {len(patterns)} patterns for {symbol}")
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
    logger.debug(f"Generating trading signals for {symbol}")
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if not data:
        logger.error(f"No market data found for symbol {symbol}")
        raise HTTPException(
            status_code=404,
            detail=f"Market data not found for symbol {symbol}"
        )

    technical_data = market_service.calculate_technical_indicators(data)
    signals = market_service.generate_signals(data, technical_data)
    logger.debug(f"Generated {len(signals)} signals for {symbol}")

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
    """
    logger.debug(f"Processing watchlist data for symbols: {symbols}")
    market_service = MarketService(db)
    results = {}

    for symbol in symbols:
        try:
            logger.debug(f"Fetching data for {symbol}")
            data = await market_service.fetch_market_data(symbol)
            if data:
                technical_data = market_service.calculate_technical_indicators(data)
                results[symbol] = {
                    "market_data": data[-1],
                    "technical_indicators": technical_data
                }
                logger.debug(f"Successfully processed {symbol}")
        except Exception as e:
            logger.error(f"Error processing {symbol}: {str(e)}")
            results[symbol] = {"error": str(e)}

    return results


@router.websocket("/ws/market/{symbol}")
async def websocket_endpoint(
        websocket: WebSocket,
        symbol: str,
        db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time market updates"""
    logger.info(f"New WebSocket connection request for {symbol}")
    connection_id = f"{symbol}_{datetime.now().timestamp()}"

    try:
        await ws_manager.connect(websocket, symbol)
        logger.debug(f"Connection {connection_id} established")

        while True:
            try:
                # Empfange Client-Nachrichten
                data = await websocket.receive_json()
                logger.debug(f"Received message from {connection_id}: {data}")

                # Verarbeite verschiedene Nachrichtentypen
                message_type = data.get('type')

                if message_type == 'subscribe':
                    await ws_manager.handle_subscription_change(websocket, data)
                elif message_type == 'timeframe_change':
                    # Implementiere Timeframe-Änderungen hier
                    pass
                elif message_type == 'ping':
                    await websocket.send_json({"type": "pong"})
                else:
                    logger.warning(f"Unknown message type from {connection_id}: {message_type}")

            except WebSocketDisconnect:
                logger.info(f"Client disconnected: {connection_id}")
                break

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from client: {connection_id}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })

            except Exception as e:
                logger.error(f"WebSocket error for {connection_id}: {str(e)}")
                try:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Internal server error"
                    })
                except:
                    break

    finally:
        logger.info(f"Cleaning up connection {connection_id}")
        await ws_manager.disconnect(websocket, symbol)