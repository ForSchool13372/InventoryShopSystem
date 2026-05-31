from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import logging

from app.core.deps import getAuthorizedGame, validatePlayer, getGame
from app.core.database import engine
from sqlalchemy import text

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# APP
# =========================================================

app = FastAPI()

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://inventoryshopsystem.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# HELPERS
# =========================================================

def ok(data):
    return {"success": True, "data": data}


def unwrap(result):
    if isinstance(result, str):
        return {"success": False, "message": result}

    if not result.get("success"):
        return {"success": False, "message": result.get("message", "Bad request")}

    return {"success": True, "message": result.get("message", "OK")}


def normalize(name: str):
    return name.strip().lower()

# =========================================================
# REQUEST MODEL
# =========================================================

class ItemRequest(BaseModel):
    itemName: str
    quantity: int

    @field_validator("itemName")
    def itemNameNotEmpty(cls, v):
        if not v.strip():
            raise ValueError("Item name cannot be empty")
        return v

    @field_validator("quantity")
    def quantityPositive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

# =========================================================
# ROUTES
# =========================================================

@app.get("/player/{playerId}")
def getPlayer(playerId: int, authorization: str = Header(default=None, alias="Authorization")):
    logger.info(f"GET /player/{playerId}")

    game = getAuthorizedGame(playerId, authorization)

    data = {
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level,
        "xp": game.player.xp
    }

    logger.info(f"PLAYER DATA SENT playerId={playerId}")

    return ok(data)


@app.post("/buy/{playerId}")
def buy(playerId: int, data: ItemRequest, authorization: str = Header(default=None, alias="Authorization")):
    logger.info(f"POST /buy/{playerId} item={data.itemName} qty={data.quantity}")

    game = getAuthorizedGame(playerId, authorization)

    result = game.buy(
        normalize(data.itemName),
        data.quantity
    )

    game.persist()

    logger.info(f"BUY RESULT playerId={playerId} result={result}")

    return ok(unwrap(result))


@app.post("/sell/{playerId}")
def sell(playerId: int, data: ItemRequest, authorization: str = Header(default=None, alias="Authorization")):
    logger.info(f"POST /sell/{playerId} item={data.itemName} qty={data.quantity}")

    game = getAuthorizedGame(playerId, authorization)

    result = game.sell(
        normalize(data.itemName),
        data.quantity
    )

    game.persist()

    logger.info(f"SELL RESULT playerId={playerId} result={result}")

    return ok(unwrap(result))


@app.get("/inventory/{playerId}")
def getInventory(playerId: int, authorization: str = Header(default=None, alias="Authorization")):
    logger.info(f"GET /inventory/{playerId}")

    game = getAuthorizedGame(playerId, authorization)

    data = game.getInventory()

    return ok({"items": data})


@app.get("/shop")
def getShop():
    logger.info("GET /shop")

    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock FROM shop")
        ).fetchall()

    data = [
        {"itemName": r[0], "stock": r[1]}
        for r in rows
    ]

    return ok(data)


@app.post("/login/{playerId}")
def login(playerId: int):
    logger.info(f"POST /login/{playerId}")

    validatePlayer(playerId)
    game = getGame(playerId)

    result = game.login()

    logger.info(f"LOGIN SUCCESS playerId={playerId}")

    return ok(result)


@app.get("/health")
def health():
    logger.info("GET /health")
    return {"status": "healthy"}