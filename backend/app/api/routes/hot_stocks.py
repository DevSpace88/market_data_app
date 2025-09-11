from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
import hashlib
import warnings

from ...models.database import get_db
from ...auth import get_current_user
from ...schemas.hot_stocks import HotStockResponse
from ...services.cache_service import cache

# Deaktiviere yfinance Debug-Logs und Warnungen
logging.getLogger('yfinance').setLevel(logging.WARNING)
logging.getLogger('peewee').setLevel(logging.WARNING)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

router = APIRouter()
logger = logging.getLogger(__name__)

# Liste der beliebten Aktien für Hot Stocks
POPULAR_SYMBOLS = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
    'ORCL', 'IBM', 'SAP', 'ASML', 'TSM', 'BABA', 'JPM', 'BAC',
    'WMT', 'JNJ', 'PG', 'KO', 'PFE', 'ABBV', 'V', 'MA', 'HD', 'DIS'
]

@router.get("/", response_model=List[HotStockResponse])
async def get_hot_stocks(
    limit: int = 20,
    sort_by: str = "change_percent",
    db: Session = Depends(get_db)
):
    """
    Get hot stocks with real market data from yfinance (cached for 15 minutes)
    """
    try:
        # Create cache key based on parameters
        cache_key = f"hot_stocks_{limit}_{sort_by}"
        
        # Check if data is cached
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Returning cached hot stocks data for key: {cache_key}")
            return cached_data
        
        logger.info(f"Cache miss for key: {cache_key}, fetching fresh data")
        hot_stocks = []
        
        # Get market data for popular symbols (limit to first 10 for speed)
        symbols_to_fetch = POPULAR_SYMBOLS[:min(limit, 10)]
        
        for symbol in symbols_to_fetch:
            try:
                # Get stock data with timeout
                stock = yf.Ticker(symbol)
                
                # Get basic info first
                info = stock.info
                company_name = info.get('longName', symbol)
                
                # Get historical data (only 2 days for speed)
                hist = stock.history(period="2d", interval="1d")
                
                if hist.empty or len(hist) < 2:
                    continue
                
                # Calculate price change
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2]
                price_change = current_price - previous_price
                change_percent = (price_change / previous_price) * 100 if previous_price != 0 else 0
                
                # Get volume
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                
                # Create chart data (use available data, pad if needed)
                chart_data = hist['Close'].tolist()
                if len(chart_data) < 7:
                    # Pad with last value if we don't have enough data
                    chart_data = [chart_data[0]] * (7 - len(chart_data)) + chart_data
                
                hot_stock = HotStockResponse(
                    symbol=symbol,
                    name=company_name,
                    price=round(current_price, 2),
                    change=round(price_change, 2),
                    change_percent=round(change_percent, 2),
                    volume=int(volume),
                    chart_data=chart_data[-7:],  # Take last 7 values
                    in_watchlist=False  # Will be updated by frontend
                )
                
                hot_stocks.append(hot_stock)
                
            except Exception as e:
                logger.warning(f"Failed to get data for {symbol}: {str(e)}")
                continue
        
        # Sort by the requested field
        if sort_by == "change_percent":
            hot_stocks.sort(key=lambda x: x.change_percent, reverse=True)
        elif sort_by == "volume":
            hot_stocks.sort(key=lambda x: x.volume, reverse=True)
        elif sort_by == "price":
            hot_stocks.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == "symbol":
            hot_stocks.sort(key=lambda x: x.symbol)
        
        result = hot_stocks[:limit]
        
        # Cache the result for 15 minutes
        cache.set(cache_key, result)
        logger.info(f"Cached {len(result)} hot stocks for key: {cache_key}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching hot stocks: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch hot stocks data")

@router.get("/trending", response_model=List[HotStockResponse])
async def get_trending_stocks(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get trending stocks (highest volume and price change) - cached for 15 minutes
    """
    try:
        # Create cache key for trending stocks
        cache_key = f"trending_stocks_{limit}"
        
        # Check if data is cached
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Returning cached trending stocks data for key: {cache_key}")
            return cached_data
        
        logger.info(f"Cache miss for trending stocks key: {cache_key}, fetching fresh data")
        
        # Get hot stocks and filter for trending ones
        hot_stocks = await get_hot_stocks(limit=50, sort_by="volume", db=db)
        
        # Filter for stocks with significant movement
        trending = [
            stock for stock in hot_stocks 
            if abs(stock.change_percent) > 2.0 and stock.volume > 1000000
        ]
        
        result = trending[:limit]
        
        # Cache the result for 15 minutes
        cache.set(cache_key, result)
        logger.info(f"Cached {len(result)} trending stocks for key: {cache_key}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching trending stocks: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending stocks data")

@router.post("/cache/clear")
async def clear_cache():
    """
    Clear hot stocks cache (admin function)
    """
    try:
        cache.clear()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear cache")

@router.get("/cache/info")
async def get_cache_info():
    """
    Get cache statistics
    """
    try:
        info = cache.get_cache_info()
        return info
    except Exception as e:
        logger.error(f"Error getting cache info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get cache info")
