from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory

gameFactory = GameFactory()

authScheme = HTTPBearer()

# =========================================================
# AUTH
# =========================================================

def getCurrentPlayerId(
    credentials: HTTPAuthorizationCredentials = Depends(authScheme)
):
    token = credentials.credentials

    payload = verifyToken(token)

    # ❌ invalid token
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # ❌ malformed payload (IMPORTANT FIX)
    if "playerId" not in payload:
        raise HTTPException(status_code=401, detail="Token missing playerId")

    return payload["playerId"]

# =========================================================
# GAME (AUTO-BINDED TO JWT USER)
# =========================================================

def getCurrentGame(
    playerId: int = Depends(getCurrentPlayerId)
):
    return gameFactory.create(playerId)