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
from app.core.database import engine
from sqlalchemy import text
from app.core.gameFactory import GameFactory

router = APIRouter(prefix="/api", tags=["Game API"])

gameFactory = GameFactory()

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
# PLAYER (FIXED: USE GAME CONTEXT NOT RANDOM DB QUERY)
# =========================================================
@router.get("/player", response_model=PlayerResponse)
def getPlayer(game=Depends(getCurrentGame)):
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                SELECT gold, hp, level, xp
                FROM player
                WHERE id = :id
            """),
            {"id": game.playerId}
        ).fetchone()

    return PlayerResponse(
        gold=row[0],
        hp=row[1],
        level=row[2],
        xp=row[3]
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
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT itemName, quantity
                FROM playerItems
                WHERE playerID = :playerId
            """),
            {"playerId": game.playerId}
        ).fetchall()

    return InventoryResponse(
        items=[
            {"itemName": r[0], "quantity": r[1]}
            for r in rows
        ]
    )

# =========================================================
# SHOP
# =========================================================
@router.get("/shop", response_model=ShopResponse)
def getShop():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock, price FROM shop")
        ).fetchall()

    return ShopResponse(
        data=[
            {"itemName": r[0], "stock": r[1], "price": r[2]}
            for r in rows
        ]
    )

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