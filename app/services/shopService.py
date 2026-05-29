class ShopService:

    # =========================================================
    # BUY
    # =========================================================

    def buy(self, player, item, quantity, playerId, shopRepo):

        self._validate_item(item)
        self._validate_quantity(quantity)

        totalCost = item.price * quantity

        if player.gold < totalCost:
            return {
                "success": False,
                "message": "Not enough gold"
            }

        if not shopRepo.hasStock(item.name, quantity):
            return {
                "success": False,
                "message": "Not enough stock"
            }

        shopRepo.decreaseStock(item.name, quantity)
        shopRepo.addOrUpdatePlayerItem(playerId, item.name, quantity)

        player.gold -= totalCost

        return {
            "success": True,
            "message": "Purchase Successful"
        }

    # =========================================================
    # SELL
    # =========================================================

    def sell(self, player, item, quantity, playerId, shopRepo):

        self._validate_item(item)
        self._validate_quantity(quantity)

        if shopRepo.getPlayerItemQuantity(playerId, item.name) < quantity:
            return {
                "success": False,
                "message": "Not enough items"
            }

        totalGain = item.price * quantity

        shopRepo.removePlayerItem(playerId, item.name, quantity)
        shopRepo.increaseStock(item.name, quantity)

        player.gold += totalGain

        return {
            "success": True,
            "message": "Sale Successful"
        }

    # =========================================================
    # VALIDATION (INTERNAL)
    # =========================================================

    def _validate_item(self, item):
        if not item:
            raise ValueError("Item does not exist")

        if not hasattr(item, "price"):
            raise ValueError("Invalid item")

    def _validate_quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Invalid quantity")