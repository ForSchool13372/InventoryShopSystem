from sqlalchemy import text
from database import engine


class ShopRepository:
    def hasStock(self, itemName, quantity):
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT stock FROM shop
                WHERE itemName = :name
            """), {
                "name": itemName.lower()
            }).fetchone()

            return result and result[0] >= quantity

    def decreaseStock(self, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE shop
                SET stock = stock - :qty
                WHERE itemName = :name
            """), {
                "qty": quantity,
                "name": itemName.lower()
            })

    def increaseStock(self, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE shop
                SET stock = stock + :qty
                WHERE itemName = :name
            """), {
                "qty": quantity,
                "name": itemName.lower()
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
                "itemName": itemName.lower(),
                "qty": quantity
            })

    def removePlayerItem(self, playerId, itemName, quantity):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE playerItems
                SET quantity = quantity - :qty
                WHERE playerID = :playerId AND itemName = :name
            """), {
                "playerId": playerId,
                "qty": quantity,
                "name": itemName.lower()
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
                WHERE playerID = :playerId AND itemName = :name
            """), {
                "playerId": playerId,
                "name": itemName.lower()
            }).fetchone()

            return result[0] if result else 0

    def getShopStock(self):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemName, stock FROM shop
            """)).fetchall()

        return [{"itemName": r[0], "stock": r[1]} for r in rows]