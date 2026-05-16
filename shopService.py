from sqlalchemy import text
from database import engine


class ShopService:
    def buy(self, player, item, quantity):

        if not item:
            return {"success": False, "message": "Item does not exist"}

        itemName = item.name.lower()

        if quantity <= 0:
            return {"success": False, "message": "Invalid quantity"}

        totalCost = item.price * quantity

        if player.gold < totalCost:
            return {"success": False, "message": "Not enough gold"}

        # check shop stock
        with engine.begin() as conn:
            stock = conn.execute(text("""
                SELECT stock FROM shop WHERE itemName = :name
            """), {"name": itemName}).fetchone()

            if not stock or stock[0] < quantity:
                return {"success": False, "message": "Not enough stock"}

            # update shop stock
            conn.execute(text("""
                UPDATE shop
                SET stock = stock - :qty
                WHERE itemName = :name
            """), {
                "qty": quantity,
                "name": itemName
            })

            # update player inventory (DB)
            conn.execute(text("""
                INSERT INTO playerItems (playerID, itemName, quantity)
                VALUES (1, :itemName, :qty)
                ON CONFLICT(playerID, itemName)
                DO UPDATE SET quantity = quantity + :qty
            """), {
                "itemName": itemName,
                "qty": quantity
            })

        player.gold -= totalCost

        return {"success": True,
               "message": "Purchase Successful",}


    def sell(self, player, item, quantity):

        if not item:
            return {"success": False, "message": "Item does not exist"}

        itemName = item.name.lower()

        if quantity <= 0:
            return {"success": False, "message": "Invalid quantity"}

        totalGain = item.price * quantity

        with engine.begin() as conn:

            # check player inventory from DB
            result = conn.execute(text("""
                SELECT quantity FROM playerItems
                WHERE playerID = 1 AND itemName = :name
            """), {"name": itemName}).fetchone()

            if not result or result[0] < quantity:
                return {"success": False, "message": "Not enough items"}

            # update player inventory
            conn.execute(text("""
                UPDATE playerItems
                SET quantity = quantity - :qty
                WHERE playerID = 1 AND itemName = :name
            """), {
                "qty": quantity,
                "name": itemName
            })

            # remove zero rows (Only for this player)
            conn.execute(text("""
                DELETE FROM playerItems
                WHERE playerID = 1 AND quantity <= 0
            """))

            # update shop stock
            conn.execute(text("""
                UPDATE shop
                SET stock = stock + :qty
                WHERE itemName = :name
            """), {
                "qty": quantity,
                "name": itemName
            })

        player.gold += totalGain

        return {"success": True,
                "message": "Sale Successful"}