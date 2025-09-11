# schemas/watchlist.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WatchlistBase(BaseModel):
    symbol: str
    display_name: Optional[str] = None

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistUpdate(BaseModel):
    symbol: Optional[str] = None
    display_name: Optional[str] = None
    is_active: Optional[bool] = None

class WatchlistResponse(WatchlistBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WatchlistWithData(WatchlistResponse):
    """Watchlist item with current market data"""
    current_price: Optional[float] = None
    price_change: Optional[float] = None
    price_change_percent: Optional[float] = None
    volume: Optional[int] = None
