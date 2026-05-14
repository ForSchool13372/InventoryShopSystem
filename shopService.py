from sqlalchemy import text
from database import engine

class ShopService:
    def __init__(self):
        pass

    def buy(self, player, item, quantity):

        #1 check if item exist
        if not item:
            return{"success": False, "message": "Item does not exist"}

        #2 Check if quantity is valid
        if quantity <= 0:
            return{"success": False, "message": "Invalid quantity"}

        # 3. Get stock from DB (source of truth)
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT stock FROM shop WHERE itemName = :name
            """), {"name": item.name.lower()}).fetchone()

        if not result or result[0] < quantity:
            return {"success": False, "message": "Not enough stock"}

        # 4. Check gold
        totalCost = item.price * quantity
        if player.gold < totalCost:
            return {"success": False, "message": "Not enough gold"}

        # 5. Apply player changes
        player.gold -= totalCost
        for _ in range(quantity):
            player.inventory.addItem(item)

        # 6. Update DB
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE shop
                SET stock = stock - :qty
                WHERE itemName = :name
            """), {
                "qty": quantity,
                "name": item.name.lower()
            })

        return {"success": True}

    def sell(self, player, item, quantity):
        # 1. Check if item exist
        if not item:
            return {"success": False, "message": "Item does not exist"}

        # 2. Check quantity is valid
        if quantity <= 0:
            return {"success": False, "message": "Not enough quantity"}

        # 3. Check if player has item
        if player.inventory.items.get(item.name.lower(), 0) < quantity:
            return {"success": False, "message": "Not enough items"}

        # 4. Calculate gain
        totalGain = item.price * quantity

        # 5. Apply player changes
        player.gold += totalGain
        for _ in range(quantity):
            player.inventory.removeItem(item)

        #6. Update DB
        with engine.begin() as conn:
          conn.execute(text("""
          UPDATE shop
          SET stock = stock + :qty
          WHERE itemName = :name
          """), {
              "qty": quantity,
              "name": item.name.lower()
              })

        return {"success": True}
