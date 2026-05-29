from sqlalchemy import text
from app.core.database import engine

class ShopRepository:

    def hasStock(self, itemName, quantity):
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT stock FROM shop
                WHERE itemName = :itemName
            """), {
                "itemName": itemName
            }).fetchone()

            return result and result[0] >= quantity

    def decreaseStock(self, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE shop
                SET stock = stock - :qty
                WHERE itemName = :itemName
            """), {
                "qty": quantity,
                "itemName": itemName
            })

    def increaseStock(self, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE shop
                SET stock = stock + :qty
                WHERE itemName = :itemName
            """), {
                "qty": quantity,
                "itemName": itemName
            })

    def addOrUpdatePlayerItem(self, playerId, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO playerItems (playerID, itemName, quantity)
                VALUES (:playerId, :itemName, :qty)
                ON CONFLICT(playerID, itemName)
                DO UPDATE SET quantity = quantity + :qty
            """), {
                "playerId": playerId,
                "itemName": itemName,
                "qty": quantity
            })

    def removePlayerItem(self, playerId, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE playerItems
                SET quantity = quantity - :qty
                WHERE playerID = :playerId AND itemName = :itemName
            """), {
                "playerId": playerId,
                "qty": quantity,
                "itemName": itemName
            })

            conn.execute(text("""
                DELETE FROM playerItems
                WHERE playerID = :playerId AND quantity <= 0
            """), {
                "playerId": playerId
            })

    def getPlayerItemQuantity(self, playerId, itemName):
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT quantity FROM playerItems
                WHERE playerID = :playerId AND itemName = :itemName
            """), {
                "playerId": playerId,
                "itemName": itemName
            }).fetchone()

            return result[0] if result else 0

    def getShopStock(self):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemName, stock FROM shop
            """)).fetchall()

        return [
            {"itemName": r[0], "stock": r[1]}
            for r in rows
        ]