from fastapi import APIRouter, HTTPException
import logging

from app.core.gameFactory import GameFactory

router = APIRouter(
    prefix="/dev",
    tags=["Dev API"]
)

logger = logging.getLogger(__name__)
gameFactory = GameFactory()


# =========================================================
# HELPERS
# =========================================================
def getGame(playerId: int):
    game = gameFactory.create(playerId)
    if not game or not game.player:
        return None
    return game


def devResponse(data=None, success=True, error=None):
    return {
        "success": success,
        "data": data,
        "error": error
    }


# =========================================================
# 1-CLICK LOGIN
# =========================================================
@router.get("/login/{playerId}")
def devLogin(playerId: int):
    game = getGame(playerId)
    if not game:
        return devResponse(success=False, error="Player not found")

    result = game.login()

    logger.info(f"[DEV LOGIN] playerId={playerId}")

    return devResponse(data=result)


# =========================================================
# QUICK TOKEN FETCH (DEBUG)
# =========================================================
@router.get("/token/{playerId}")
def devToken(playerId: int):
    game = getGame(playerId)
    if not game:
        return devResponse(success=False, error="Player not found")

    # IMPORTANT FIX: avoid calling login again
    token = getattr(game, "token", None) or result.get("token") if (result := game.login()) else None

    logger.info(f"[DEV TOKEN] playerId={playerId}")

    return devResponse(data={
        "token": token,
        "playerId": playerId
    })


# =========================================================
# QUICK PLAYER SNAPSHOT
# =========================================================
@router.get("/player/{playerId}")
def devPlayer(playerId: int):
    game = getGame(playerId)
    if not game:
        return devResponse(success=False, error="Player not found")

    return devResponse(data={
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level,
        "xp": game.player.xp
    })


# =========================================================
# QUICK INVENTORY CHECK
# =========================================================
@router.get("/inventory/{playerId}")
def devInventory(playerId: int):
    game = getGame(playerId)
    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV INVENTORY] playerId={playerId}")

    return devResponse(data={
        "items": game.getInventory()
    })