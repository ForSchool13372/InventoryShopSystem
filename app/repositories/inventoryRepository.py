from sqlalchemy import text
from app.core.database import engine

class InventoryRepository:

    def loadInventory(self, playerId):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemName, quantity
                FROM playerItems
                WHERE playerID = :playerId
            """),{
                    "playerId": playerId
                }).fetchall()

        return [{"itemName": r[0], "quantity": r[1]} for r in rows]

    def saveInventory(self, playerId, inventoryDict):
        with engine.begin() as conn:
            #Clear old inventory
            conn.execute(text("""
                DELETE from playerItems
                WHERE playerID = :playerId
            """),{
                    "playerId": playerId
                })

            #Reinsert fresh state
            for itemName, qty in inventoryDict.items():
                conn.execute(text("""
                    INSERT INTO playerItems (playerID, itemName, quantity)
                    VALUES (:playerId, :itemName, :qty)
                """),{
                        "playerId": playerId,
                        "itemName": itemName,
                        "qty": qty
                    })