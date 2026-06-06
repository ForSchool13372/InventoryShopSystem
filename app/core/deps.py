from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory

authScheme = HTTPBearer()


def getGameFactory():
    return GameFactory()


def getCurrentPlayerId(
    credentials: HTTPAuthorizationCredentials = Depends(authScheme)
):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = credentials.credentials
    payload = verifyToken(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    playerId = payload.get("playerId")

    if playerId is None:
        raise HTTPException(status_code=401, detail="Missing playerId")

    return playerId


def getCurrentGame(
    playerId: int = Depends(getCurrentPlayerId),
    factory: GameFactory = Depends(getGameFactory)
):
    return factory.create(playerId)