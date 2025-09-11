# app/api/routes/websocket.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from ...models.database import get_db
from ...services.websocket_manager import WebSocketManager
from ...auth import get_token_from_ws_query, verify_ws_token

router = APIRouter()
ws_manager = WebSocketManager()


@router.get("/info")
async def websocket_general_info():
    """
    Get general WebSocket connection information.
    
    **WebSocket Endpoints:**
    - Market data: `ws://localhost:8000/api/v1/ws/market/{symbol}?token=YOUR_JWT_TOKEN`
    
    **Authentication:** JWT token required as query parameter for all WebSocket connections.
    
    **Available Symbols:** Any valid stock symbol (e.g., NVDA, AAPL, TSLA)
    """
    return {
        "websocket_endpoints": {
            "market_data": "ws://localhost:8000/api/v1/ws/market/{symbol}?token=YOUR_JWT_TOKEN"
        },
        "authentication": "JWT token required as query parameter",
        "message_types": ["subscribe", "timeframe_change", "ping"],
        "example_connection": "ws://localhost:8000/api/v1/ws/market/NVDA?token=your_jwt_token"
    }


@router.get("/market/{symbol}/info")
async def websocket_info(symbol: str):
    """
    Get WebSocket connection information for a symbol.
    
    **WebSocket Endpoint:** `ws://localhost:8000/api/v1/ws/market/{symbol}?token=YOUR_JWT_TOKEN`
    
    **Authentication:** Include your JWT token as a query parameter.
    
    **Message Types:**
    - `subscribe`: Subscribe to real-time updates
    - `timeframe_change`: Change the timeframe
    - `ping`: Ping the server (will receive `pong` response)
    
    **Example Connection:**
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/api/v1/ws/market/NVDA?token=your_jwt_token');
    ```
    """
    return {
        "websocket_url": f"ws://localhost:8000/api/v1/ws/market/{symbol}",
        "authentication": "JWT token required as query parameter",
        "message_types": ["subscribe", "timeframe_change", "ping"],
        "symbol": symbol
    }


@router.websocket("/market/{symbol}")
async def websocket_endpoint(
        websocket: WebSocket,
        symbol: str,
        db: Session = Depends(get_db)
):
    # Auth for WebSocket
    token = await get_token_from_ws_query(websocket)
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return

    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=4001, reason="Invalid authentication token")
        return

    # Accept the connection
    await websocket.accept()

    connection_id = f"{symbol}_{datetime.now().timestamp()}"
    try:
        await ws_manager.connect(websocket, symbol)
        while True:
            try:
                data = await websocket.receive_json()
                message_type = data.get('type')

                if message_type == 'subscribe':
                    await ws_manager.handle_subscription_change(websocket, data)
                elif message_type == 'timeframe_change':
                    pass  # Handle timeframe changes
                elif message_type == 'ping':
                    await websocket.send_json({"type": "pong"})

            except WebSocketDisconnect:
                break
            except Exception as e:
                logging.error(f"WebSocket error: {str(e)}")
                try:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Internal server error"
                    })
                except:
                    break
    finally:
        await ws_manager.disconnect(websocket, symbol)