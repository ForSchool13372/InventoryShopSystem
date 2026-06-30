from fastapi import APIRouter
import logging

from app.core.game.gameFactory import GameFactory

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
    if not game:
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

    logger.info(f"[DEV LOGIN] playerid={playerId}")

    return devResponse(data=result)


# =========================================================
# QUICK PLAYER SNAPSHOT
# =========================================================
@router.get("/player/{playerId}")
def devPlayer(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    return devResponse(data=game.getPlayerStats())


# =========================================================
# QUICK INVENTORY CHECK
# =========================================================
@router.get("/inventory/{playerId}")
def devInventory(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV INVENTORY] playerid={playerId}")

    return devResponse(data={
        "items": game.getInventory()
    })


# =========================================================
# FIGHT (DEV)
# =========================================================
@router.post("/fight/{playerId}")
async def devFight(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV FIGHT] playerid={playerId}")

    result = await game.fight()

    return devResponse(data=result)


# =========================================================
# BUY (DEV)
# =========================================================
@router.post("/buy/{playerId}")
async def devBuy(playerId: int, itemName: str, quantity: int = 1):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV BUY] playerid={playerId} item={itemName} qty={quantity}")

    result = await game.buy(itemName, quantity)

    return devResponse(data=result)


# =========================================================
# SELL (DEV)
# =========================================================
@router.post("/sell/{playerId}")
async def devSell(playerId: int, itemName: str, quantity: int = 1):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV SELL] playerid={playerId} item={itemName} qty={quantity}")

    result = await game.sell(itemName, quantity)

    return devResponse(data=result)


# =========================================================
# SHOP (DEV)
# =========================================================
@router.get("/shop/{playerId}")
def devShop(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV SHOP] playerid={playerId}")

    return devResponse(data=game.shop.getShop())


# =========================================================
# EVENTS (DEV)
# =========================================================
@router.get("/events/{playerId}")
def devEvents(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV EVENTS] playerid={playerId}")

    return devResponse(data={
        "events": game.gameEventService.getEvents()
    })

# =========================================================
# QUESTS (DEV)
# =========================================================
@router.get("/quests/{playerId}")
def devQuests(playerId: int):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV QUESTS] playerid={playerId}")

    return devResponse(data={
        "quests": [
            q.getStatus() for q in game.questManager.quests
        ]
    })


# =========================================================
# CLAIM QUEST (DEV)
# =========================================================
@router.post("/quests/claim/{playerId}")
async def devClaimQuest(playerId: int, questName: str):
    game = getGame(playerId)

    if not game:
        return devResponse(success=False, error="Player not found")

    logger.info(f"[DEV CLAIM QUEST] playerid={playerId} quest={questName}")

    result = await game.claimQuest(questName)

    return devResponse(data=result)