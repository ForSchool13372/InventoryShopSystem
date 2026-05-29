from fastapi import Header, HTTPException

from app.core.auth import verifyToken
from app.core.gameFactory import GameFactory
from app.core.database import engine

from sqlalchemy import text

gameFactory = GameFactory()

# =========================================================
# AUTH
# =========================================================

def getCurrentPlayer(
    authorization: str = Header(default=None, alias="Authorization")
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = verifyToken(authorization)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["playerId"]


# =========================================================
# VALIDATION
# =========================================================

def validatePlayer(playerId: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT 1 FROM player WHERE id = :id"),
            {"id": playerId}
        ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Player does not exist")


# =========================================================
# GAME
# =========================================================

def getGame(playerId: int):
    return gameFactory.create(playerId)


# =========================================================
# AUTHORIZED GAME
# =========================================================

def getAuthorizedGame(
    playerId: int,
    authorization: str = Header(default=None, alias="Authorization")
):
    validatePlayer(playerId)

    authPlayerId = getCurrentPlayer(authorization)

    if authPlayerId != playerId:
        raise HTTPException(status_code=403, detail="Not your player")

    return getGame(playerId)