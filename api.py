from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
from database import engine
from controller import Controller

app = FastAPI()

def getGame(playerId: int):
    return Controller(playerId)

class BuyRequest(BaseModel):
    itemName: str
    quantity: int


# ---------------- PLAYER ----------------
@app.get("/player/{playerId}")
def getPlayer(playerId: int):
    game = getGame(playerId)

    return {
        "success": True,
        "data": {
            "gold": game.player.gold,
            "hp": game.player.hp,
            "level": game.player.level
        }
    }


# ---------------- BUY ----------------
@app.post("/buy/{playerId}")
def buy(playerId: int, data: BuyRequest):
    game = getGame(playerId)

    if not data.itemName.strip():
        return {
            "success": False,
            "data": {"message": "Item name cannot be empty"}
        }

    if data.quantity <= 0:
        return {
            "success": False,
            "data": {"message": "Quantity must be greater than 0"}
        }

    return game.buy(data.itemName, data.quantity)


# ---------------- INVENTORY ----------------
@app.get("/inventory/{playerId}")
def getInventory(playerId: int):
    game = getGame(playerId)

    return {
        "success": True,
        "data": {
            "items": game.getInventory()
        }
    }


# ---------------- SHOP ----------------
@app.get("/shop")
def getShop():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT itemName, stock FROM shop")
        ).fetchall()

    return {
        "success": True,
        "data": [
            {"itemName": r[0], "stock": r[1]}
            for r in rows
        ]
    }