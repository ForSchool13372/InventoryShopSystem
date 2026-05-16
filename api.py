from fastapi import FastAPI
from controller import Controller
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

app = FastAPI()
game = Controller()

class BuyRequest(BaseModel):
    itemName: str
    quantity: int

@app.get("/player")
def getPlayer():
    return {
        "success": True,
        "data": {
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level
        }
    }

@app.post("/buy")
def buy(data: BuyRequest):
    if not data.itemName or not data.itemName.strip():
        return {
                "success": False,
                "data": {
                    "message": "Item name cannot be empty"
                    }
            }

    if data.quantity <= 0:
        return {
            "success": False,
            "data": {
            "message": "Quantity must be greater than 0"
                }
            }

    result = game.buy(data.itemName, data.quantity)

    if not result["success"]:
        return result

    return{
        "success": True,
        "data": {
        "itemName": data.itemName,
        "quantity": data.quantity,
        "gold": game.player.gold,
        "hp": game.player.hp,
        "level": game.player.level
            }
        }

@app.get("/inventory")
def getInventory():
    return {
        "success": True,
        "data":{
        "items": game.getInventory()
            }
        }

@app.get("/shop")
def getShop():
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT itemName, stock FROM shop")).fetchall()

        return {
            "success": True,
            "data": [
                {"itemName": r[0], "stock": r[1]}
                for r in rows
                ]
        }
    except Exception:
        return {
            "success": False,
            "data": {
                    "message": "Failed to fetch shop data"
                }
            }
