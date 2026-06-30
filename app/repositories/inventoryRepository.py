from sqlalchemy import text
from app.core.database import engine


class InventoryRepository:

    def loadInventory(self, playerId: int):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT 
                    p.itemname,
                    p.quantity,
                    s.itemtype,
                    s.rarity,
                    s.description,
                    s.price
                FROM playeritems p
                JOIN shop s ON s.itemname = p.itemname
                WHERE p.playerid = :playerid
            """), {"playerid": playerId}).mappings().all()

            return [
                {
                    "itemName": r["itemname"],
                    "quantity": r["quantity"],
                    "itemType": r["itemtype"],
                    "rarity": r["rarity"],
                    "description": r["description"],
                    "price": r["price"]
                }
                for r in rows
            ]


    def saveInventory(self, playerId: int, inventoryDict: dict):
        with engine.begin() as conn:
            conn.execute(text("""
                DELETE FROM playeritems
                WHERE playerid = :playerid
            """), {
                "playerid": playerId
            })

            for itemName, qty in inventoryDict.items():
                conn.execute(text("""
                    INSERT INTO playeritems (playerid, itemname, quantity)
                    VALUES (:playerid, :itemname, :qty)
                """), {
                    "playerid": playerId,
                    "itemname": itemName,
                    "qty": qty
                })