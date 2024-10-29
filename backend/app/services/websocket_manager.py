from fastapi import WebSocket
from typing import Dict, Set
import asyncio
import json
from .market_service import MarketService
from ..models.database import get_db


class WebSocketManager:
    def __init__(self):
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._tasks: Dict[str, asyncio.Task] = {}

        async def connect(self, websocket: WebSocket, symbol: str):
            await websocket.accept()
            if symbol not in self._connections:
                self._connections[symbol] = set()
                self._tasks[symbol] = asyncio.create_task(
                    self._update_symbol(symbol)
                )
            self._connections[symbol].add(websocket)

        async def disconnect(self, websocket: WebSocket, symbol: str):
            if symbol in self._connections:
                self._connections[symbol].discard(websocket)
                if not self._connections[symbol] and symbol in self._tasks:
                    self._tasks[symbol].cancel()
                    del self._tasks[symbol]
                    del self._connections[symbol]
            await websocket.close()

        async def broadcast(self, symbol: str, message: dict):
            if symbol not in self._connections:
                return

            dead_connections = set()
            for connection in self._connections[symbol]:
                try:
                    await connection.send_json(message)
                except:
                    dead_connections.add(connection)

            # Cleanup dead connections
            for dead in dead_connections:
                self._connections[symbol].discard(dead)

        async def _update_symbol(self, symbol: str):
            """Background task to update market data"""
            try:
                while True:
                    if symbol not in self._connections:
                        break

                    db = next(get_db())
                    market_service = MarketService(db)
                    data = await market_service.fetch_market_data(symbol, "1m")

                    if data:
                        await self.broadcast(
                            symbol,
                            {
                                "type": "market_update",
                                "symbol": symbol,
                                "data": data
                            }
                        )

                    await asyncio.sleep(1)  # Update interval
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error in update task for {symbol}: {e}")
            finally:
                if symbol in self._connections:
                    del self._connections[symbol]
                if symbol in self._tasks:
                    del self._tasks[symbol]