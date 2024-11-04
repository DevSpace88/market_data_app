# app/api/routes/market.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from ...models.database import get_db
from ...services.market_service import MarketService
from ...services.ai_analysis_service import MarketAIAnalysis
from ...auth import get_current_active_user, User

router = APIRouter()
market_ai = MarketAIAnalysis()
market_ai.set_debug(True)


@router.get("/data/{symbol}")
async def get_market_data(
        symbol: str,
        timeframe: str = Query("1d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    market_service = MarketService(db)
    data = await market_service.fetch_market_data(symbol, timeframe)
    if not data:
        raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/analysis/{symbol}")
async def get_market_analysis(
        symbol: str,
        timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
        include_news: bool = Query(True),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    try:
        market_service = MarketService(db)
        timeframe_map = {
            "1D": ("1d", "5m"),
            "1W": ("7d", "1h"),
            "1M": ("1mo", "1d"),
            "3M": ("3mo", "1d"),
            "6M": ("6mo", "1d"),
            "1Y": ("1y", "1d"),
            "YTD": ("ytd", "1d")
        }
        period, interval = timeframe_map.get(timeframe, ("1mo", "1h"))

        market_data = await market_service.fetch_market_data(symbol, period=period, interval=interval)
        if not market_data:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        technical_data = market_service.calculate_technical_indicators(market_data)
        patterns = await market_service.detect_patterns(market_data)
        signals = market_service.generate_signals(market_data, technical_data)

        ai_analysis = await market_ai.generate_market_summary(
            symbol=symbol,
            market_data=market_data,
            technical_data=technical_data,
            patterns=patterns
        )

        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_data": market_data,
            "technical_indicators": technical_data,
            "patterns": patterns,
            "signals": signals,
            "ai_analysis": ai_analysis,
            "timeframe": timeframe
        }

    except Exception as e:
        logging.error(f"Error in market analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analyzing market data: {str(e)}")


