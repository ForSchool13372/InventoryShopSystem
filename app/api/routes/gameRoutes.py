from fastapi import APIRouter, Depends
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
from app.core.gameFactory import GameFactory

# repos
from app.repositories.inventoryRepository import InventoryRepository

router = APIRouter(prefix="/api", tags=["Game API"])

gameFactory = GameFactory()
inventoryRepository = InventoryRepository()

# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    def action():
        result = gameFactory.create(data.playerId).login()
        return LoginResponse(**result)

    return safeExecute(action)


# =========================================================
# PLAYER
# =========================================================
@router.get("/player", response_model=PlayerResponse)
def getPlayer(game=Depends(getCurrentGame)):
    return PlayerResponse(
        gold=game.player.gold,
        hp=game.player.hp,
        level=game.player.level,
        xp=game.player.xp
    )


# =========================================================
# BUY
# =========================================================
@router.post("/buy")
def buy(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        return game.buy(
            normalize(data.itemName),
            data.quantity
        )

    return safeExecute(action)


# =========================================================
# SELL
# =========================================================
@router.post("/sell")
def sell(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        return game.sell(
            normalize(data.itemName),
            data.quantity
        )

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