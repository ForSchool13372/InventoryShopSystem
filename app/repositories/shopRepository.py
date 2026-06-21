from sqlalchemy import text


class ShopRepository:

    # =========================================================
    # SHOP
    # =========================================================

    def getShopStock(self, conn):
        rows = conn.execute(text("""
            SELECT itemname, stock, price
            FROM shop
        """)).mappings().all()

        return [dict(row) for row in rows]

    def getStock(self, conn, itemName: str):
        result = conn.execute(
            text("""
                SELECT stock
                FROM shop
                WHERE itemname = :itemname
            """),
            {"itemname": itemName}
        ).mappings().fetchone()

        return {"stock": result["stock"] if result else 0}

    # =========================================================
    # PLAYER ITEMS
    # =========================================================

    def getPlayerItemQuantity(self, conn, playerId: int, itemName: str):
        result = conn.execute(text("""
            SELECT quantity
            FROM playeritems
            WHERE playerid = :playerid AND itemname = :itemname
        """), {
            "playerid": playerId,
            "itemname": itemName
        }).mappings().fetchone()

        return {"quantity": result["quantity"] if result else 0}

    def addOrUpdatePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
        conn.execute(text("""
            INSERT INTO playeritems (playerid, itemname, quantity)
            VALUES (:playerid, :itemname, :qty)
            ON CONFLICT (playerid, itemname)
            DO UPDATE SET quantity = playeritems.quantity + EXCLUDED.quantity
        """), {
            "playerid": playerId,
            "itemname": itemName,
            "qty": quantity
        })

    def removePlayerItem(self, conn, playerId: int, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE playeritems
            SET quantity = quantity - :qty
            WHERE playerid = :playerid AND itemname = :itemname
        """), {
            "playerid": playerId,
            "itemname": itemName,
            "qty": quantity
        })

        conn.execute(text("""
            DELETE FROM playeritems
            WHERE playerid = :playerid AND quantity <= 0
        """), {
            "playerid": playerId
        })

    # =========================================================
    # SHOP STOCK
    # =========================================================

    def decreaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock - :qty
            WHERE itemname = :itemname
        """), {
            "qty": quantity,
            "itemname": itemName
        })

    def increaseStock(self, conn, itemName: str, quantity: int):
        conn.execute(text("""
            UPDATE shop
            SET stock = stock + :qty
            WHERE itemname = :itemname
        """), {
            "qty": quantity,
            "itemname": itemName
        })