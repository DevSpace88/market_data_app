# app/api/routes/market.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging
import yfinance as yf

from ...models.database import get_db
from ...services.market_service import MarketService
from ...services.ai_analysis_service import MarketAIAnalysis
from ...auth import get_current_active_user, User

logger = logging.getLogger(__name__)

router = APIRouter()
market_ai = MarketAIAnalysis()
market_ai.set_debug(True)


# @router.get("/data/{symbol}")
# async def get_market_data(
#         symbol: str,
#         timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     market_service = MarketService(db)
#     data = await market_service.fetch_market_data(symbol, timeframe)
#     if not data:
#         raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#     return {
#         "symbol": symbol,
#         "timeframe": timeframe,
#         "data": data,
#         "timestamp": datetime.now().isoformat()
#     }

# # hat funktionineert aber nichts angezeigt
# @router.get("/data/{symbol}")
# async def get_market_data(
#         symbol: str,
#         timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     try:
#         market_service = MarketService(db)
#         data = await market_service.fetch_market_data(symbol, timeframe)
#         if not data:
#             raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
#
#         # Basis-Response ohne Währungsinfo
#         response = {
#             "symbol": symbol,
#             "timeframe": timeframe,
#             "data": data,
#             "timestamp": datetime.now().isoformat()
#         }
#
#         # Optional: Versuche Währungsinfo zu bekommen
#         try:
#             stock = yf.Ticker(symbol)
#             quote_type = stock.info.get('quoteType', {})
#             currency = quote_type.get('currency', 'USD')
#
#             currency_symbols = {
#                 'USD': '$',
#                 'JPY': '¥',
#                 'EUR': '€',
#                 'GBP': '£',
#                 'CNY': '¥',
#                 'HKD': 'HK$',
#                 'KRW': '₩'
#             }
#
#             response.update({
#                 "currency": currency,
#                 "currencySymbol": currency_symbols.get(currency, '$')
#             })
#         except Exception as currency_error:
#             logger.warning(f"Could not fetch currency info for {symbol}: {str(currency_error)}")
#             response.update({
#                 "currency": "USD",
#                 "currencySymbol": "$"
#             })
#
#         return response
#
#     except Exception as e:
#         logger.error(f"Error in get_market_data: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# app/api/routes/market.py
@router.get("/data/{symbol}")
async def get_market_data(
        symbol: str,
        timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    try:
        # Währungsbestimmung basierend auf Symbol-Suffix
        currency = "USD"
        currency_symbol = "$"

        if symbol.endswith('.T'):  # Japanische Börse
            currency = "JPY"
            currency_symbol = "¥"
        elif symbol.endswith('.L'):  # London
            currency = "GBP"
            currency_symbol = "£"
        elif symbol.endswith('.HK'):  # Hong Kong
            currency = "HKD"
            currency_symbol = "HK$"
        elif symbol.endswith('.KS'):  # Korea
            currency = "KRW"
            currency_symbol = "₩"
        elif symbol.endswith('.SS') or symbol.endswith('.SZ'):  # Shanghai/Shenzhen
            currency = "CNY"
            currency_symbol = "¥"

        market_service = MarketService(db)
        data = await market_service.fetch_market_data(symbol, timeframe)
        if not data:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "data": data,
            "currency": currency,
            "currencySymbol": currency_symbol,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in get_market_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/analysis/{symbol}")
# async def get_market_analysis(
#         symbol: str,
#         timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
#         include_news: bool = Query(True),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     try:
#         market_service = MarketService(db)
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
#         logging.error(f"Error in market analysis: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Error analyzing market data: {str(e)}")


# app/api/routes/market.py

# Alte Analyse-Route entfernt, um Konflikte mit neuer strukturierter Analyse zu vermeiden

# kp ob das noch nötig ist?
@router.get("/validate/{symbol}")
async def validate_symbol(
        symbol: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Validiere ein Symbol bevor die volle Analyse startet"""
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Symbol {symbol} not found or data unavailable"
        )

    return {"valid": True, "symbol": symbol}

@router.get("/search")
async def search_stocks(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Suche nach Stocks basierend auf Symbol oder Name"""
    logger.debug(f"Search request for query: {query}")
    market_service = MarketService(db)
    results = await market_service.search_stocks(query)
    logger.debug(f"Found {len(results)} results for {query}")
    return results