from fastapi import APIRouter, Depends, WebSocket
import asyncio

from app.api.routes.schemas.gameSchemas import (
    ItemRequest,
    LoginRequest,
    PlayerResponse,
    ShopResponse,
    InventoryResponse,
    LoginResponse
)

from app.core.utils.apiUtils import safeExecute
from app.core.deps import getCurrentGame
from app.core.utils.rateLimiter import rateLimiter

from app.core.wsManager import wsManager
from app.repositories.inventoryRepository import InventoryRepository
from app.repositories.playerRepository import PlayerRepository
from app.services.leaderboardService import LeaderboardService


router = APIRouter(prefix="/api", tags=["Game API"])

inventoryRepository = InventoryRepository()
playerRepository = PlayerRepository()
leaderboardService = LeaderboardService(playerRepository)

# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    return safeExecute(lambda: LoginResponse(**getCurrentGame(data.playerId).login()))


# =========================================================
# PLAYER
# =========================================================
@router.get("/player", response_model=PlayerResponse)
def getPlayer(game=Depends(getCurrentGame)):
    player = game.getPlayerStats()

    return PlayerResponse(
        gold=player["gold"],
        hp=player["hp"],
        level=player["level"],
        xp=player["xp"]
    )


# =========================================================
# BUY
# =========================================================
@router.post("/buy")
def buy(
    data: ItemRequest,
    game=Depends(getCurrentGame),
    allowed=Depends(rateLimiter("buy"))
):
    if not allowed:
        return {"error": "Too many requests"}

    return safeExecute(
        lambda: game.buy(
            data.itemName,
            data.quantity
        )
    )


# =========================================================
# SELL
# =========================================================
@router.post("/sell")
def sell(
    data: ItemRequest,
    game=Depends(getCurrentGame),
    allowed=Depends(rateLimiter("sell"))
):
    if not allowed:
        return {"error": "Too many requests"}

    return safeExecute(
        lambda: game.sell(
            data.itemName,
            data.quantity
        )
    )


# =========================================================
# INVENTORY
# =========================================================
@router.get("/inventory", response_model=InventoryResponse)
def getInventory(game=Depends(getCurrentGame)):
    rows = inventoryRepository.loadInventory(game.playerId)

    return InventoryResponse(
        items=[
            {"itemName": r["itemName"], "quantity": r["quantity"]}
            for r in rows
        ]
    )


# =========================================================
# SHOP
# =========================================================
@router.get("/shop", response_model=ShopResponse)
def getShop(game=Depends(getCurrentGame)):
    return ShopResponse(data=game.shop.getShop())


# =========================================================
# EVENTS
# =========================================================
@router.get("/events")
def getEvents(game=Depends(getCurrentGame)):
    return {"events": game.eventService.getEvents()}


# =========================================================
# HEALTH
# =========================================================
@router.get("/health")
def health():
    return {"status": "healthy"}


# =========================================================
# LEADERBOARD WEBSOCKET
# =========================================================
@router.websocket("/ws/leaderboard")
async def leaderboardSocket(websocket: WebSocket):
    await wsManager.connect(websocket)

    try:
        while True:
            await websocket.send_json({
                "type": "LEADERBOARD_UPDATE",
                "data": leaderboardService.getLeaderboard()
            })
            await asyncio.sleep(5)

    except Exception:
        pass

    finally:
        wsManager.disconnect(websocket)