from pydantic import BaseModel
from typing import List, Optional

class HotStockResponse(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    chart_data: List[float]
    in_watchlist: bool = False
    
    class Config:
        from_attributes = True
