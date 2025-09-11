# api/routes/watchlist.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...models.database import get_db
from ...models.user import User
from ...models.watchlist import Watchlist
from ...schemas.watchlist import WatchlistCreate, WatchlistUpdate, WatchlistResponse, WatchlistWithData
from ...auth import get_current_active_user
from ...services.market_service import MarketService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[WatchlistResponse])
async def get_watchlist(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's watchlist"""
    watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.is_active == True
    ).all()
    return watchlist

@router.get("/with-data", response_model=List[WatchlistWithData])
async def get_watchlist_with_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's watchlist with current market data"""
    watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.is_active == True
    ).all()
    
    result = []
    for item in watchlist:
        try:
            # Get current market data
            market_data = MarketService.get_market_data(item.symbol, "1D")
            if market_data and market_data.get("price"):
                current_price = market_data["price"]
                # Calculate price change (simplified - you might want to store previous close)
                price_change = 0  # This would need to be calculated properly
                price_change_percent = 0
                volume = market_data.get("volume", 0)
            else:
                current_price = None
                price_change = None
                price_change_percent = None
                volume = None
        except Exception as e:
            logger.warning(f"Failed to get market data for {item.symbol}: {e}")
            current_price = None
            price_change = None
            price_change_percent = None
            volume = None
        
        watchlist_item = WatchlistWithData(
            id=item.id,
            user_id=item.user_id,
            symbol=item.symbol,
            display_name=item.display_name,
            is_active=item.is_active,
            created_at=item.created_at,
            updated_at=item.updated_at,
            current_price=current_price,
            price_change=price_change,
            price_change_percent=price_change_percent,
            volume=volume
        )
        result.append(watchlist_item)
    
    return result

@router.post("/", response_model=WatchlistResponse)
async def add_to_watchlist(
    watchlist_item: WatchlistCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add symbol to watchlist"""
    # Check if symbol already exists in user's watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.symbol == watchlist_item.symbol.upper(),
        Watchlist.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol already in watchlist"
        )
    
    # Create new watchlist item
    db_watchlist = Watchlist(
        user_id=current_user.id,
        symbol=watchlist_item.symbol.upper(),
        display_name=watchlist_item.display_name
    )
    
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    
    logger.info(f"Added {watchlist_item.symbol} to watchlist for user {current_user.username}")
    return db_watchlist

@router.put("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist_item(
    watchlist_id: int,
    watchlist_update: WatchlistUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update watchlist item"""
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    
    # Update fields
    update_data = watchlist_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "symbol" and value:
            value = value.upper()
        setattr(watchlist_item, field, value)
    
    db.commit()
    db.refresh(watchlist_item)
    
    logger.info(f"Updated watchlist item {watchlist_id} for user {current_user.username}")
    return watchlist_item

@router.delete("/{watchlist_id}")
async def remove_from_watchlist(
    watchlist_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove symbol from watchlist (soft delete)"""
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    
    # Soft delete
    watchlist_item.is_active = False
    db.commit()
    
    logger.info(f"Removed {watchlist_item.symbol} from watchlist for user {current_user.username}")
    return {"message": "Symbol removed from watchlist"}

@router.delete("/symbol/{symbol}")
async def remove_symbol_from_watchlist(
    symbol: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove symbol from watchlist by symbol name"""
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.symbol == symbol.upper(),
        Watchlist.is_active == True
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symbol not found in watchlist"
        )
    
    # Soft delete
    watchlist_item.is_active = False
    db.commit()
    
    logger.info(f"Removed {symbol} from watchlist for user {current_user.username}")
    return {"message": f"Symbol {symbol} removed from watchlist"}
