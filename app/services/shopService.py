class ShopService:

    # =========================================================
    # PUBLIC API
    # =========================================================

    def buy(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        total_cost = ctx.item.price * ctx.quantity

        if ctx.player.gold < total_cost:
            return self._fail("Not enough gold")

        if not ctx.shopRepo.hasStock(ctx.item.name, ctx.quantity):
            return self._fail("Not enough stock")

        ctx.shopRepo.decreaseStock(ctx.item.name, ctx.quantity)
        ctx.shopRepo.addOrUpdatePlayerItem(
            ctx.playerId,
            ctx.item.name,
            ctx.quantity
        )

        ctx.player.gold -= total_cost

        return self._success("Purchase Successful")

    def sell(self, ctx):
        self._validate_item(ctx.item)
        self._validate_quantity(ctx.quantity)

        if ctx.shopRepo.getPlayerItemQuantity(ctx.playerId, ctx.item.name) < ctx.quantity:
            return self._fail("Not enough items")

        total_gain = ctx.item.price * ctx.quantity

        ctx.shopRepo.removePlayerItem(
            ctx.playerId,
            ctx.item.name,
            ctx.quantity
        )

        ctx.shopRepo.increaseStock(ctx.item.name, ctx.quantity)

        ctx.player.gold += total_gain

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
        return {
            "success": True,
            "message": message
        }

    def _fail(self, message):
        return {
            "success": False,
            "message": message
        }