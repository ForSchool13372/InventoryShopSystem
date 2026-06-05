from sqlalchemy import text
from app.core.database import engine


class ShopRepository:

    # =========================================================
    # STOCK CHECKS (NOW SAFE OBJECT RETURNS)
    # =========================================================

    def getStock(self, conn, itemName: str):
        result = conn.execute(
            text("""
                SELECT stock
                FROM shop
                WHERE itemName = :itemName
            """),
            {"itemName": itemName}
        ).fetchone()

        if not result:
            return {"stock": 0}

        return {"stock": result[0]}

    def getPlayerItemQuantity(self, conn, playerId: int, itemName: str):
        result = conn.execute(
            text("""
                SELECT quantity
                FROM playerItems
                WHERE playerID = :playerId AND itemName = :itemName
            """),
            {
                "playerId": playerId,
                "itemName": itemName
            }
        ).fetchone()

        if not result:
            return {"quantity": 0}

        return {"quantity": result[0]}

    # =========================================================
    # SHOP STOCK OPS
    # =========================================================

    def decreaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(
            text("""
                UPDATE shop
                SET stock = stock - :qty
                WHERE itemName = :itemName
            """),
            {
                "qty": quantity,
                "itemName": itemName
            }
        )

    def increaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(
            text("""
                UPDATE shop
                SET stock = stock + :qty
                WHERE itemName = :itemName
            """),
            {
                "qty": quantity,
                "itemName": itemName
            }
        )

    # =========================================================
    # PLAYER ITEMS OPS
    # =========================================================

    def addOrUpdatePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
        conn.execute(
            text("""
                INSERT INTO playerItems (playerID, itemName, quantity)
                VALUES (:playerId, :itemName, :qty)
                ON CONFLICT (playerID, itemName)
                DO UPDATE SET quantity = playerItems.quantity + EXCLUDED.quantity
            """),
            {
                "playerId": playerId,
                "itemName": itemName,
                "qty": quantity
            }
        )

    def removePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
        conn.execute(
            text("""
                UPDATE playerItems
                SET quantity = quantity - :qty
                WHERE playerID = :playerId AND itemName = :itemName
            """),
            {
                "playerId": playerId,
                "qty": quantity,
                "itemName": itemName
            }
        )

        conn.execute(
            text("""
                DELETE FROM playerItems
                WHERE playerID = :playerId AND quantity <= 0
            """),
            {"playerId": playerId}
        )

    # =========================================================
    # READ ONLY
    # =========================================================

    def getShopStock(self):
        with engine.begin() as conn:
            rows = conn.execute(
                text("""
                    SELECT itemName, stock
                    FROM shop
                """)
            ).fetchall()

        return [
            {"itemName": r[0], "stock": r[1]}
            for r in rows
        ]