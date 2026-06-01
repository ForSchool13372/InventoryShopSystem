from functools import lru_cache
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory

authScheme = HTTPBearer()

# =========================================================
# FACTORY (SAFE SINGLETON VIA CACHE)
# =========================================================

@lru_cache
def getGameFactory():
    """
    Create GameFactory once and reuse it.
    Prevents re-initialization per request and avoids import-time issues.
    """
    return GameFactory()

# =========================================================
# AUTH
# =========================================================

def getCurrentPlayerId(
    credentials: HTTPAuthorizationCredentials = Depends(authScheme)
):
    token = credentials.credentials

    payload = verifyToken(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if "playerId" not in payload:
        raise HTTPException(status_code=401, detail="Token missing playerId")

    return payload["playerId"]

# =========================================================
# GAME (PER REQUEST CONTEXT)
# =========================================================

def getCurrentGame(
    playerId: int = Depends(getCurrentPlayerId),
    factory: GameFactory = Depends(getGameFactory)
):
    """
    Build game instance safely per request using cached factory.
    """
    try:
        return factory.create(playerId)
    except Exception as e:
        # prevents silent 500 + CORS confusion
        raise HTTPException(status_code=500, detail=str(e))