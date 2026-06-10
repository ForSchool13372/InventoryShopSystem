from typing import Set
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.activeConnections: Set[WebSocket] = set()

    # =========================================================
    # CONNECTION MANAGEMENT
    # =========================================================
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activeConnections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activeConnections.discard(websocket)

    # =========================================================
    # CORE BROADCAST
    # =========================================================
    async def broadcast(self, data: dict):
        if not self.activeConnections:
            return

        deadConnections = set()

        for connection in list(self.activeConnections):
            try:
                await connection.send_json(data)
            except Exception:
                deadConnections.add(connection)

        for dc in deadConnections:
            self.activeConnections.discard(dc)

    # =========================================================
    # LEADERBOARD SAFE FORMAT (IMPORTANT FIX)
    # =========================================================
    async def broadcastLeaderboard(self, leaderboard: list):
        await self.broadcast({
            "type": "LEADERBOARD_UPDATE",
            "data": list(leaderboard)  # ensures always array-safe
        })


# =========================================================
# SINGLETON (IMPORTANT)
# =========================================================
wsManager = WSManager()