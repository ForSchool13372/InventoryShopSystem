from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
import logging
import time
from functools import wraps

from app.core.deps import getCurrentGame
from app.core.gameFactory import GameFactory
from app.core.database import engine
from sqlalchemy import text

# =========================================================
# INIT
# =========================================================
router = APIRouter(
    prefix="/api",
    tags=["Game API"]
)

logger = logging.getLogger(__name__)
gameFactory = GameFactory()

SLOW_REQUEST_MS = 100

# =========================================================
# RESPONSE HELPERS
# =========================================================
def ok(data):
    return {"success": True, "data": data}

def fail(message: str):
    return {"success": False, "message": message}

def normalize(name: str):
    return name.strip().lower()

def handle_result(result):
    if isinstance(result, str):
        return fail(result)

    if isinstance(result, dict) and result.get("success") is False:
        return fail(result.get("message", "Error"))

    return ok(result)

# =========================================================
# OBSERVABILITY
# =========================================================
def monitor(routeName: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            success = True

            try:
                return func(*args, **kwargs)

            except Exception:
                success = False
                logger.exception(f"{routeName} FAILED")
                raise

            finally:
                duration = round((time.time() - start) * 1000, 2)
                status = "OK" if success else "ERROR"

                msg = f"{routeName} | {status} | {duration}ms"
                if duration > SLOW_REQUEST_MS:
                    msg += " | SLOW_REQUEST"

                logger.info(msg)

        return wrapper
    return decorator

# =========================================================
# REQUEST MODELS
# =========================================================
class ItemRequest(BaseModel):
    itemName: str
    quantity: int

    @field_validator("itemName")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Item name cannot be empty")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_qty(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be > 0")
        return v


class LoginRequest(BaseModel):
    playerId: int

# =========================================================
# ROUTES
# =========================================================
@router.post("/login")
@monitor("POST /login")
def login(data: LoginRequest):
    try:
        game = gameFactory.create(data.playerId)
        result = game.login()
        return ok(result)

    except ValueError as e:
        logger.warning(f"LOGIN FAILED | playerId={data.playerId} | {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        logger.exception(f"LOGIN CRASHED | playerId={data.playerId}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/player")
@monitor("GET /player")
def getPlayer(game=Depends(getCurrentGame)):
    return ok({
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level,
        "xp": game.player.xp
    })


@router.post("/buy")
@monitor("POST /buy")
def buy(data: ItemRequest, game=Depends(getCurrentGame)):
    try:
        result = game.buy(
            normalize(data.itemName),
            data.quantity
        )

        game.persist()
        return handle_result(result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        logger.exception(f"BUY CRASHED | item={data.itemName}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/sell")
@monitor("POST /sell")
def sell(data: ItemRequest, game=Depends(getCurrentGame)):
    try:
        result = game.sell(
            normalize(data.itemName),
            data.quantity
        )

        game.persist()
        return handle_result(result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        logger.exception(f"SELL CRASHED | item={data.itemName}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/inventory")
@monitor("GET /inventory")
def getInventory(game=Depends(getCurrentGame)):
    return ok({"items": game.getInventory()})


@router.get("/shop")
@monitor("GET /shop")
def getShop():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock, price FROM shop")
        ).fetchall()

    return ok([
        {
            "itemName": r[0],
            "stock": r[1],
            "price": r[2]
        }
        for r in rows
    ])


@router.get("/events")
@monitor("GET /events")
def getEvents(game=Depends(getCurrentGame)):
    return ok({"events": game.eventService.getEvents()})


@router.get("/health")
@monitor("GET /health")
def health():
    return {"status": "healthy"}