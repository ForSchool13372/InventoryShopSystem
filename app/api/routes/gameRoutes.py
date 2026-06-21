from fastapi import APIRouter, Depends, WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
import logging
from typing import Set
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
from app.core.deps import getCurrentGame, getCurrentGameWs
from app.core.utils.rateLimiter import rateLimiter

from app.core.wsManager import wsManager
from app.repositories.inventoryRepository import InventoryRepository
from app.repositories.playerRepository import PlayerRepository
from app.services.leaderboardService import LeaderboardService


router = APIRouter(prefix="/api", tags=["Game API"])

inventoryRepository = InventoryRepository()
playerRepository = PlayerRepository()
leaderboardService = LeaderboardService(playerRepository)
logger = logging.getLogger(__name__)


# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    return safeExecute(
        lambda: LoginResponse(**getCurrentGame(data.playerId).login())
    )


# =========================================================
# PLAYER
# =========================================================
@router.get("/player", response_model=PlayerResponse)
def getPlayer(game=Depends(getCurrentGame)):
    try:
        return PlayerResponse(**game.getPlayerStats())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =========================================================
# FIGHT (NEW)
# =========================================================
@router.post("/fight")
def fight(game=Depends(getCurrentGame)):
    return safeExecute(
        lambda: game.fight()
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
        lambda: game.buy(data.itemName, data.quantity)
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
        lambda: game.sell(data.itemName, data.quantity)
    )


# =========================================================
# INVENTORY
# =========================================================
@router.get("/inventory", response_model=InventoryResponse)
def getInventory(game=Depends(getCurrentGame)):
    rows = inventoryRepository.loadInventory(game.playerId)

    return InventoryResponse(items=rows)


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
    return {"events": game.gameEventService.getEvents()}


# =========================================================
# HEALTH
# =========================================================
@router.get("/health")
def health():
    return {"status": "healthy"}


# =========================================================
# LEADERBOARD WEBSOCKET (EVENT-DRIVEN)
# =========================================================
@router.websocket("/ws/leaderboard")
async def leaderboardSocket(websocket: WebSocket):
    await wsManager.connect(websocket)

    try:
        leaderboard = leaderboardService.getLeaderboard()

        await websocket.send_json({
            "type": "LEADERBOARD_UPDATE",
            "data": leaderboard
        })

        while True:
            await asyncio.sleep(5)

            leaderboard = leaderboardService.getLeaderboard()

            await websocket.send_json({
                "type": "LEADERBOARD_UPDATE",
                "data": leaderboard
            })

    except WebSocketDisconnect:
        logger.info("Client disconnected from leaderboard websocket")

    except Exception as e:
        logger.exception("Leaderboard websocket error")

    finally:
        wsManager.disconnect(websocket)