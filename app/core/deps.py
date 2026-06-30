from fastapi import HTTPException, Depends, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.game.gameFactory import GameFactory
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

    # 🔥 If game already exists in memory → reuse it
    if playerId in gameState.games:
        return gameState.games[playerId]

    # 🔥 First time → create and store
    game = factory.create(playerId)
    gameState.games[playerId] = game

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

    if playerId in gameState.games:
        return gameState.games[playerId]

    game = factory.create(playerId)
    gameState.games[playerId] = game
    return game
