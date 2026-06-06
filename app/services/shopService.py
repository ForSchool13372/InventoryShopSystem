from sqlalchemy import text
from app.core.database import engine


class ShopService:

    def buy(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        itemName = ctx.item.name
        quantity = ctx.quantity
        playerId = ctx.playerId

        totalCost = ctx.item.price * quantity

        if ctx.player.gold < totalCost:
            return self._fail("Not enough gold")

        with engine.begin() as conn:

            stock = ctx.shopRepo.getStock(conn, itemName)

            if stock["stock"] < quantity:
                return self._fail("Not enough stock")

            ctx.shopRepo.decreaseStock(conn, itemName, quantity)

            ctx.shopRepo.addOrUpdatePlayerItem(
                conn,
                playerId,
                itemName,
                quantity
            )

            conn.execute(text("""
                UPDATE player
                SET gold = gold - :cost
                WHERE id = :id
            """), {
                "cost": totalCost,
                "id": playerId
            })

        ctx.player.gold -= totalCost

        return self._success("Purchase Successful")

    def sell(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        itemName = ctx.item.name
        quantity = ctx.quantity
        playerId = ctx.playerId

        totalGain = ctx.item.price * quantity

        with engine.begin() as conn:

            owned = ctx.shopRepo.getPlayerItemQuantity(conn, playerId, itemName)

            if owned["quantity"] < quantity:
                return self._fail("Not enough items")

            ctx.shopRepo.removePlayerItem(
                conn,
                playerId,
                itemName,
                quantity
            )

            ctx.shopRepo.increaseStock(conn, itemName, quantity)

            conn.execute(text("""
                UPDATE player
                SET gold = gold + :gain
                WHERE id = :id
            """), {
                "gain": totalGain,
                "id": playerId
            })

        ctx.player.gold += totalGain

        return self._success("Sale Successful")

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_item(self, item):
        if item is None:
            raise ValueError("Item does not exist")

        if not hasattr(item, "price"):
            raise ValueError("Invalid item")

    def _validate_quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Invalid quantity")

    # =========================================================
    # RESPONSE HELPERS
    # =========================================================

    def _success(self, message):
        return {"success": True, "message": message}

    def _fail(self, message):
        return {"success": False, "message": message}