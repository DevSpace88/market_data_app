from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MarketDataBase(BaseModel):
    symbol: str
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float

class MarketDataCreate(MarketDataBase):
    pass

class MarketDataResponse(MarketDataBase):
    id: int

    class Config:
        from_attributes = True