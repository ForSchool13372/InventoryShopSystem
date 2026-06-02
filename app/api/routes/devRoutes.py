from fastapi import APIRouter
import logging

from app.core.gameFactory import GameFactory

router = APIRouter(
    prefix="/dev",
    tags=["Dev API"]
)

logger = logging.getLogger(__name__)
gameFactory = GameFactory()

# =========================================================
# 1-CLICK LOGIN (NO BODY, NO SWAGGER FRICTION)
# =========================================================
@router.get("/login/{playerId}")
def devLogin(playerId: int):
    game = gameFactory.create(playerId)
    result = game.login()

    logger.info(f"[DEV LOGIN] playerId={playerId}")

    return {
        "success": True,
        "data": result
    }


# =========================================================
# QUICK TOKEN FETCH (OPTIONAL DEBUG TOOL)
# =========================================================
@router.get("/token/{playerId}")
def devToken(playerId: int):
    game = gameFactory.create(playerId)
    result = game.login()

    logger.info(f"[DEV TOKEN] playerId={playerId}")

    return {
        "token": result.get("token"),
        "playerId": playerId
    }


# =========================================================
# QUICK PLAYER SNAPSHOT (NO AUTH REQUIRED)
# =========================================================
@router.get("/player/{playerId}")
def devPlayer(playerId: int):
    game = gameFactory.create(playerId)

    return {
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level,
        "xp": game.player.xp
    }


# =========================================================
# QUICK INVENTORY CHECK
# =========================================================
@router.get("/inventory/{playerId}")
def devInventory(playerId: int):
    game = gameFactory.create(playerId)

    return {
        "items": game.getInventory()
    }