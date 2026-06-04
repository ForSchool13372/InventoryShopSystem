from sqlalchemy import text
from app.core.database import engine


class ShopRepository:

    # =========================================================
    # COMBINED FAST CHECK (NO EXTRA CONNECTIONS)
    # =========================================================

    def getStock(self, conn, itemName):
        return conn.execute(text("""
            SELECT stock
            FROM shop
            WHERE itemName = :itemName
        """), {"itemName": itemName}).fetchone()

    def getPlayerItemQuantity(self, conn, playerId, itemName):
        result = conn.execute(text("""
            SELECT quantity
            FROM playerItems
            WHERE playerID = :playerId AND itemName = :itemName
        """), {
            "playerId": playerId,
            "itemName": itemName
        }).fetchone()

        return result[0] if result else 0

    # =========================================================
    # SHOP STOCK (FAST OPS)
    # =========================================================

    def decreaseStock(self, conn, itemName, quantity):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock - :qty
            WHERE itemName = :itemName
        """), {
            "qty": quantity,
            "itemName": itemName
        })

    def increaseStock(self, conn, itemName, quantity):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock + :qty
            WHERE itemName = :itemName
        """), {
            "qty": quantity,
            "itemName": itemName
        })

    # =========================================================
    # PLAYER ITEMS (FAST OPS)
    # =========================================================

    def addOrUpdatePlayerItem(self, conn, playerId, itemName, quantity):
        conn.execute(text("""
            INSERT INTO playerItems (playerID, itemName, quantity)
            VALUES (:playerId, :itemName, :qty)
            ON CONFLICT (playerID, itemName)
            DO UPDATE SET quantity = playerItems.quantity + EXCLUDED.quantity
        """), {
            "playerId": playerId,
            "itemName": itemName,
            "qty": quantity
        })

    def removePlayerItem(self, conn, playerId, itemName, quantity):
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

    # =========================================================
    # READ ONLY (SAFE)
    # =========================================================

    def getShopStock(self):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemName, stock
                FROM shop
            """)).fetchall()

        return [
            {"itemName": r[0], "stock": r[1]}
            for r in rows
        ]