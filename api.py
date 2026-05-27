from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, field_validator
from fastapi.middleware.cors import CORSMiddleware
from auth import verifyToken
from gameFactory import GameFactory
from database import engine
from sqlalchemy import text

# =========================================================
# APP
# =========================================================

app = FastAPI()

gameFactory = GameFactory()

#Security layer which websites can talk to my backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================================
# HELPERS
# =========================================================

def ok(data):
    return {"success": True, "data": data}


def handleResult(result):
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Bad request"))
    return {"message": result["message"]}


def getCurrentPlayer(token: str = Header(default=None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = verifyToken(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["playerId"]


def validatePlayerId(playerId: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT 1 FROM player WHERE id = :id"),
            {"id": playerId}
        ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Player does not exist")


def authorizePlayer(playerId: int, token: str):
    validatePlayerId(playerId)

    authPlayerId = getCurrentPlayer(token)
    if authPlayerId != playerId:
        raise HTTPException(status_code=403, detail="Not your player")


def normalizeItemName(name: str):
    return name.strip().lower()


# =========================================================
# REQUEST MODELS
# =========================================================

class BuyRequest(BaseModel):
    itemName: str
    quantity: int

    #Field validator, checks if data is correct
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
# GAME FACTORY ACCESS
# =========================================================

def getGame(playerId: int):
    return gameFactory.create(playerId)


# =========================================================
# ROUTES
# =========================================================

@app.get("/player/{playerId}")
def getPlayer(playerId: int, token: str = Header(default=None)):
    authorizePlayer(playerId, token)

    game = getGame(playerId)

    return ok({
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level
    })


@app.post("/buy/{playerId}")
def buy(playerId: int, data: BuyRequest, token: str = Header(default=None)):
    authorizePlayer(playerId, token)

    game = getGame(playerId)

    itemName = normalizeItemName(data.itemName)
    result = game.buy(itemName, data.quantity)

    game.persist()

    return ok(handleResult(result))

@app.post("/sell/{playerId}")
def sell(playerId: int, data: BuyRequest, token: str = Header(default=None)):
    authorizePlayer(playerId, token)

    game = getGame(playerId)

    itemName = normalizeItemName(data.itemName)
    result = game.sell(itemName, data.quantity)

    game.persist()

    return ok(handleResult(result))

@app.get("/inventory/{playerId}")
def getInventory(playerId: int, token: str = Header(default=None)):
    authorizePlayer(playerId, token)

    game = getGame(playerId)

    return ok({
        "items": game.getInventory()
    })


@app.get("/shop")
def getShop():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock FROM shop")
        ).fetchall()

    return ok([
        {"itemName": r[0], "stock": r[1]}
        for r in rows
    ])


@app.post("/login/{playerId}")
def login(playerId: int):
    validatePlayerId(playerId)

    game = getGame(playerId)

    return ok(game.login())