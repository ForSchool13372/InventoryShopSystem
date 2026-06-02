from functools import lru_cache
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory

authScheme = HTTPBearer()

# =========================================================
# FACTORY (SAFE SINGLETON VIA CACHE)
# =========================================================

@lru_cache
def getGameFactory():
    return GameFactory()


# =========================================================
# AUTH
# =========================================================

def getCurrentPlayerId(
    credentials: HTTPAuthorizationCredentials = Depends(authScheme)
):
    """
    Extract and validate playerId from JWT token.
    """

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing auth token"
        )

    token = credentials.credentials

    payload = verifyToken(token)

    # clearer failure reason (not just "Invalid token")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    playerId = payload.get("playerId")

    if playerId is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing playerId"
        )

    return playerId


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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Game creation failed: {str(e)}"
        )