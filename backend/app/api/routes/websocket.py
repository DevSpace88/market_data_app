# app/api/routes/websocket.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from ...models.database import get_db
from ...services.websocket_manager import WebSocketManager
from ...auth import get_token_from_ws_query, verify_ws_token

router = APIRouter()
ws_manager = WebSocketManager()


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