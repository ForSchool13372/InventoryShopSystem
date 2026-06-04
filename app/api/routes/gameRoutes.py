from fastapi import APIRouter, Depends, HTTPException
from app.api.routes.schemas.gameSchemas import ItemRequest, LoginRequest
from app.core.utils.apiUtils import ok, normalize, safeExecute
import logging
import time
from functools import wraps

from app.core.deps import getCurrentGame
from app.core.gameFactory import GameFactory
from app.core.database import engine
from sqlalchemy import text

# =========================
# INIT
# =========================
router = APIRouter(
    prefix="/api",
    tags=["Game API"]
)

logger = logging.getLogger(__name__)
gameFactory = GameFactory()

SLOW_REQUEST_MS = 100

# =========================
# ROUTES
# =========================
@router.post("/login")
def login(data: LoginRequest):
    return safeExecute(lambda: ok(
        gameFactory.create(data.playerId).login()
    ))


@router.get("/player")
def getPlayer(game=Depends(getCurrentGame)):
    return ok({
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level,
        "xp": game.player.xp
    })


@router.post("/buy")
def buy(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        result = game.buy(
            normalize(data.itemName),
            data.quantity
        )
        game.persist()
        return result

    return safeExecute(lambda: ok(action()))


@router.post("/sell")
def sell(data: ItemRequest, game=Depends(getCurrentGame)):
    def action():
        result = game.sell(
            normalize(data.itemName),
            data.quantity
        )
        game.persist()
        return result

    return safeExecute(lambda: ok(action()))


@router.get("/inventory")
def getInventory(game=Depends(getCurrentGame)):
    return ok({"items": game.getInventory()})


@router.get("/shop")
def getShop():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock, price FROM shop")
        ).fetchall()

    return ok([
        {"itemName": r[0], "stock": r[1], "price": r[2]}
        for r in rows
    ])


@router.get("/events")
def getEvents(game=Depends(getCurrentGame)):
    return ok({"events": game.eventService.getEvents()})


@router.get("/health")
def health():
    return {"status": "healthy"}