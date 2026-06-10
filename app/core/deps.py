from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory

authScheme = HTTPBearer()

# single shared factory (IMPORTANT FIX)
factory = GameFactory()


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


def getCurrentGame(playerId: int = Depends(getCurrentPlayerId)):
    return factory.create(playerId)