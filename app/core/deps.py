from fastapi import HTTPException, Depends, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory
from app.state.gameState import gameState

authScheme = HTTPBearer()
factory = GameFactory()


# =========================================================
# HTTP AUTH
# =========================================================
def getCurrentPlayerId(
    credentials: HTTPAuthorizationCredentials = Depends(authScheme)
):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing auth token")

    payload = verifyToken(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    playerId = payload.get("playerId")

    if playerId is None:
        raise HTTPException(status_code=401, detail="Missing playerId")

    return playerId


# =========================================================
# FIXED GAME LOADER (IMPORTANT PART)
# =========================================================
def getCurrentGame(playerId: int = Depends(getCurrentPlayerId)):

    # 🔥 If player already exists in memory → reuse it
    if gameState.hasPlayer(playerId):
        player = gameState.getPlayer(playerId)

        # wrap existing player into controller again
        return factory.create(playerId)

    # 🔥 First time login → create + store in memory
    game = factory.create(playerId)

    gameState.addPlayer(playerId, game.ctx.player)

    return game


# =========================================================
# WEBSOCKET SAFE VERSION
# =========================================================
def getWebsocketPlayerId(token: str):
    payload = verifyToken(token)

    if payload is None:
        return None

    return payload.get("playerId")


def getCurrentGameWs(token: str):
    playerId = getWebsocketPlayerId(token)

    if not playerId:
        return None

    return factory.create(playerId)