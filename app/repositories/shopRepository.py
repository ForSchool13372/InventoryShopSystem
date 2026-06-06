from sqlalchemy import text


class ShopRepository:

    def getShopStock(self, conn):
        rows = conn.execute(text("""
            SELECT itemName, stock, price
            FROM shop
        """)).fetchall()

        return [
            {
                "itemName": r[0],
                "stock": r[1],
                "price": r[2]
            }
            for r in rows
        ]

    def getStock(self, conn, itemName: str):
        result = conn.execute(
            text("SELECT stock FROM shop WHERE itemName = :itemName"),
            {"itemName": itemName}
        ).fetchone()

        return {"stock": result[0] if result else 0}

    def getPlayerItemQuantity(self, conn, playerId: int, itemName: str):
        result = conn.execute(text("""
            SELECT quantity
            FROM playerItems
            WHERE playerID = :playerId AND itemName = :itemName
        """), {
            "playerId": playerId,
            "itemName": itemName
        }).fetchone()

        return {"quantity": result[0] if result else 0}

    def decreaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock - :qty
            WHERE itemName = :itemName
        """), {
            "qty": quantity,
            "itemName": itemName
        })

    def increaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock + :qty
            WHERE itemName = :itemName
        """), {
            "qty": quantity,
            "itemName": itemName
        })

    def addOrUpdatePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
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

    def removePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE playerItems
            SET quantity = quantity - :qty
            WHERE playerID = :playerId AND itemName = :itemName
        """), {
            "playerId": playerId,
            "itemName": itemName,
            "qty": quantity
        })

        conn.execute(text("""
            DELETE FROM playerItems
            WHERE playerID = :playerId AND quantity <= 0
        """), {
            "playerId": playerId
        })