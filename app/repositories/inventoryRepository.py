from sqlalchemy import text
from app.core.database import engine


class InventoryRepository:

    def loadInventory(self, playerId: int):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemname, quantity
                FROM playeritems
                WHERE playerid = :playerid
            """), {"playerid": playerId}).mappings().all()

            return [
                {
                    "itemName": r["itemname"],
                    "quantity": r["quantity"]
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