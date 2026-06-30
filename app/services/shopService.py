from sqlalchemy import text
from app.core.database import engine


class ShopService:

    def __init__(self, shopRepo):
        self.shopRepo = shopRepo

    # =========================================================
    # SHOP VIEW
    # =========================================================
    def getShop(self):
        with engine.begin() as conn:
            return self.shopRepo.getShopStock(conn)

    # =========================================================
    # BUY
    # =========================================================
    def buy(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        itemName = ctx.item["itemName"]
        quantity = ctx.quantity
        playerId = ctx.playerId

        totalCost = ctx.item["price"] * quantity

        if ctx.player.core["gold"] < totalCost:
            return self._fail("Not enough gold")

        with engine.begin() as conn:

            stock = self.shopRepo.getStock(conn, itemName)
            if not stock or stock.get("stock", 0) < quantity:
                return self._fail("Not enough stock")

            self.shopRepo.decreaseStock(conn, itemName, quantity)

            self.shopRepo.addOrUpdatePlayerItem(
                conn,
                playerId,
                itemName,
                quantity
            )

            conn.execute(
                text("""
                    UPDATE player
                    SET gold = gold - :cost
                    WHERE id = :id
                """),
                {"cost": totalCost, "id": playerId}
            )

        return {
            "success": True,
            "message": "Purchase Successful",
            "cost": totalCost
        }

    # =========================================================
    # SELL
    # =========================================================
    def sell(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        itemName = ctx.item["itemName"]
        quantity = ctx.quantity
        playerId = ctx.playerId

        totalGain = ctx.item["price"] * quantity

        with engine.begin() as conn:

            owned = self.shopRepo.getPlayerItemQuantity(conn, playerId, itemName)

            if not owned or owned.get("quantity", 0) < quantity:
                return self._fail("Not enough items")

            self.shopRepo.removePlayerItem(
                conn,
                playerId,
                itemName,
                quantity
            )

            self.shopRepo.increaseStock(conn, itemName, quantity)

            conn.execute(
                text("""
                    UPDATE player
                    SET gold = gold + :gain
                    WHERE id = :id
                """),
                {"gain": totalGain, "id": playerId}
            )

        return {
            "success": True,
            "message": "Sale Successful",
            "gain": totalGain
        }

    # =========================================================
    # VALIDATION
    # =========================================================
    def _validate_item(self, item):
        if not item:
            raise ValueError("Item does not exist")

        if not isinstance(item, dict):
            raise ValueError("Invalid item type")

        # normalize casing safely
        if "itemName" not in item:
            if "itemname" in item:
                item["itemName"] = item["itemname"]
            else:
                raise ValueError("Invalid item structure")

        if "price" not in item:
            raise ValueError("Invalid item structure")

    def _validate_quantity(self, quantity):
        if quantity is None or quantity <= 0:
            raise ValueError("Invalid quantity")

    # =========================================================
    # RESPONSE HELPERS
    # =========================================================
    def _success(self, message):
        return {"success": True, "message": message}

    def _fail(self, message):
        return {"success": False, "message": message}