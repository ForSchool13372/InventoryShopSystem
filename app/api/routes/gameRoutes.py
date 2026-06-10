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

from app.core.utils.apiUtils import normalize, safeExecute
from app.core.deps import getCurrentGame

from app.core.wsManager import wsManager
from app.state.gameState import gameState

from app.repositories.inventoryRepository import InventoryRepository
from app.repositories.playerRepository import PlayerRepository

router = APIRouter(prefix="/api", tags=["Game API"])

inventoryRepository = InventoryRepository()
playerRepository = PlayerRepository()


# =========================================================
# REAL-TIME HELPERS
# =========================================================

def getGlobalLeaderboard():
    players = playerRepository.getAll()
    return sorted(
        players,
        key=lambda p: (p["level"], p["xp"], p["gold"]),
        reverse=True
    )


# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    def action():
        game = getCurrentGame(data.playerId)
        result = game.login()
        return LoginResponse(**result)

    return safeExecute(action)


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
def buy(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        result = game.buy(
            normalize(data.itemName),
            data.quantity
        )

        return result

    return safeExecute(action)


# =========================================================
# SELL
# =========================================================
@router.post("/sell")
def sell(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        result = game.sell(
            normalize(data.itemName),
            data.quantity
        )

        return result

    return safeExecute(action)


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
    shop = game.shop.getShop()
    return ShopResponse(data=shop)


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
                "data": getGlobalLeaderboard()
            })

            await asyncio.sleep(5)

    except Exception:
        pass

    finally:
        wsManager.disconnect(websocket)
