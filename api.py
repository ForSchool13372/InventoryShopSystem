from fastapi import FastAPI
from controller import Controller
from pydantic import BaseModel

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
    items = []

    for name, qty in game.shop.stock.items():
        items.append({
            "itemName": name,
            "stock": qty
        })

    return {
        "success": True,
        "data": items
    }