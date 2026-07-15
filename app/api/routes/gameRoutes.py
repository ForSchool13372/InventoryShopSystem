from fastapi import APIRouter, Depends, WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
import logging

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


# =========================================================
# ROUTER SETUP
# =========================================================
router = APIRouter(prefix="/api", tags=["Game API"])

logger = logging.getLogger(__name__)

# Global service instances
inventoryRepository = InventoryRepository()
playerRepository = PlayerRepository()
leaderboardService = LeaderboardService(playerRepository)


# =========================================================
# AUTH / LOGIN
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

@router.get("/player/{playerId}", response_model=PlayerResponse)
def getPlayerById(playerId: int):
    game = getCurrentGame(playerId)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return PlayerResponse(**game.getPlayerStats())


# =========================================================
# COMBAT
# =========================================================
@router.post("/fight")
async def fight(game=Depends(getCurrentGame)):
    return await game.fight()


# =========================================================
# SHOP ACTIONS
# =========================================================
@router.post("/buy")
async def buy(
    data: ItemRequest,
    game=Depends(getCurrentGame),
    allowed=Depends(rateLimiter("buy"))
):
    if not allowed:
        return {"error": "Too many requests"}

    return await game.buy(data.itemName, data.quantity)


@router.post("/sell")
async def sell(
    data: ItemRequest,
    game=Depends(getCurrentGame),
    allowed=Depends(rateLimiter("sell"))
):
    if not allowed:
        return {"error": "Too many requests"}

    return await game.sell(data.itemName, data.quantity)


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
# HEALTH CHECK
# =========================================================
@router.get("/health")
def health():
    return {"status": "healthy"}


# =========================================================
# WEBSOCKET - LEADERBOARD
# =========================================================
@router.websocket("/ws/leaderboard")
async def leaderboardSocket(websocket: WebSocket):
    await wsManager.connect(websocket)

    try:
        # initial push
        await wsManager.broadcastLeaderboard(
            leaderboardService.getLeaderboard()
        )

        # keep connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        pass

    finally:
        wsManager.disconnect(websocket)

# =========================================================
# Quests
# =========================================================
@router.get("/quests")
def getQuests(game=Depends(getCurrentGame)):
    return {
        "quests": [
            q.getStatus() for q in game.questManager.quests
        ]
    }

@router.post("/quests/claim/{questName}")
async def claimQuest(
    questName: str,
    game=Depends(getCurrentGame)
):
    return await game.claimQuest(questName)