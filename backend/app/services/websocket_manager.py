from fastapi import WebSocket
from typing import Dict, Set, List  # List hinzugefügt
import asyncio
import logging

from .market_service import MarketService
from ..models.database import get_db

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._tasks: Dict[str, asyncio.Task] = {}
        self.update_interval = 5  # Sekunden zwischen Updates
        logger.info("WebSocket Manager initialized")

    async def connect(self, websocket: WebSocket, symbol: str):
        """Verbindung für ein Symbol herstellen"""
        logger.debug(f"New connection request for symbol {symbol}")
        try:
            await websocket.accept()
            if symbol not in self._connections:
                self._connections[symbol] = set()
                self._tasks[symbol] = asyncio.create_task(
                    self._update_symbol(symbol)
                )
            self._connections[symbol].add(websocket)
            logger.info(f"Connection established for {symbol}. Active connections: {len(self._connections[symbol])}")

            # Sende initiales Update
            await self._send_initial_data(websocket, symbol)

        except Exception as e:
            logger.error(f"Error establishing connection for {symbol}: {str(e)}")
            if websocket in self._connections.get(symbol, set()):
                self._connections[symbol].remove(websocket)

    async def disconnect(self, websocket: WebSocket, symbol: str):
        """Verbindung für ein Symbol trennen"""
        logger.debug(f"Disconnecting {symbol}")
        try:
            if symbol in self._connections:
                self._connections[symbol].discard(websocket)
                logger.debug(f"Removed connection for {symbol}")

                # Wenn keine Verbindungen mehr, Task beenden
                if not self._connections[symbol]:
                    if symbol in self._tasks:
                        logger.info(f"Cancelling update task for {symbol}")
                        self._tasks[symbol].cancel()
                        del self._tasks[symbol]
                    del self._connections[symbol]
            await websocket.close()

        except Exception as e:
            logger.error(f"Error during disconnect for {symbol}: {str(e)}")

    async def broadcast_to_symbol(self, symbol: str, message: dict):
        """Nachricht an alle Verbindungen eines Symbols senden"""
        if symbol not in self._connections:
            return

        dead_connections = set()
        active_connections = self._connections[symbol].copy()

        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection for {symbol}: {str(e)}")
                dead_connections.add(connection)

        # Cleanup tote Verbindungen
        for dead in dead_connections:
            self._connections[symbol].discard(dead)
            logger.debug(f"Removed dead connection for {symbol}")

    async def _send_initial_data(self, websocket: WebSocket, symbol: str):
        """Initiales Datenpaket senden"""
        try:
            db = next(get_db())
            market_service = MarketService(db)
            data = await market_service.fetch_market_data(symbol, "1d")
            if data:
                await websocket.send_json({
                    "type": "initial_data",
                    "symbol": symbol,
                    "data": data
                })
        except Exception as e:
            logger.error(f"Error sending initial data for {symbol}: {str(e)}")

    async def _update_symbol(self, symbol: str):
        """Background Task für Symbol-Updates"""
        logger.info(f"Starting update task for {symbol}")
        try:
            while True:
                if symbol not in self._connections:
                    logger.debug(f"No more connections for {symbol}, stopping updates")
                    break

                try:
                    db = next(get_db())
                    market_service = MarketService(db)
                    data = await market_service.fetch_market_data(symbol, "1m")

                    if data:
                        # Technische Indikatoren berechnen
                        technical_data = market_service.calculate_technical_indicators(data)

                        # Muster erkennen
                        patterns = await market_service.detect_patterns(data)

                        # Trading Signale generieren
                        signals = market_service.generate_signals(data, technical_data)

                        await self.broadcast_to_symbol(
                            symbol,
                            {
                                "type": "market_update",
                                "symbol": symbol,
                                "timestamp": data[-1]['timestamp'] if data else None,
                                "data": data[-100:],  # Letzte 100 Datenpunkte
                                "technical": technical_data,
                                "patterns": patterns,
                                "signals": signals
                            }
                        )
                        logger.debug(f"Sent update for {symbol}")

                except Exception as e:
                    logger.error(f"Error in update loop for {symbol}: {str(e)}")

                await asyncio.sleep(self.update_interval)

        except asyncio.CancelledError:
            logger.info(f"Update task cancelled for {symbol}")
        except Exception as e:
            logger.error(f"Unexpected error in update task for {symbol}: {str(e)}")
        finally:
            if symbol in self._connections:
                del self._connections[symbol]
            if symbol in self._tasks:
                del self._tasks[symbol]
            logger.info(f"Cleanup completed for {symbol}")

    async def handle_subscription_change(self, websocket: WebSocket, data: dict):
        """Behandelt Änderungen der Subscription"""
        try:
            symbol = data.get('symbol')
            action = data.get('action')  # 'subscribe' oder 'unsubscribe'

            if action == 'subscribe':
                await self.connect(websocket, symbol)
            elif action == 'unsubscribe':
                await self.disconnect(websocket, symbol)

        except Exception as e:
            logger.error(f"Error handling subscription change: {str(e)}")

    def get_active_connections(self, symbol: str = None) -> int:
        """Gibt die Anzahl aktiver Verbindungen zurück"""
        if symbol:
            return len(self._connections.get(symbol, set()))
        return sum(len(connections) for connections in self._connections.values())

    def get_active_symbols(self) -> List[str]:
        """Gibt eine Liste aller aktiven Symbole zurück"""
        return list(self._connections.keys())