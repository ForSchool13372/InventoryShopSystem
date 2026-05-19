class ShopService:
    def buy(self, player, item, quantity, playerId, shopRepo):
        if not item:
            return {"success": False, "message": "Item does not exist"}

        if quantity <= 0:
            return {"success": False, "message": "Invalid quantity"}

        totalCost = item.price * quantity

        if player.gold < totalCost:
            return {"success": False, "message": "Not enough gold"}

        if not shopRepo.hasStock(item.name, quantity):
            return {"success": False, "message": "Not enough stock"}

        # APPLY CHANGES VIA REPO
        shopRepo.decreaseStock(item.name, quantity)
        shopRepo.addOrUpdatePlayerItem(playerId, item.name, quantity)

        player.gold -= totalCost

        return {"success": True, "message": "Purchase Successful"}


    def sell(self, player, item, quantity, playerId, shopRepo):
        if not item:
            return {"success": False, "message": "Item does not exist"}

        if quantity <= 0:
            return {"success": False, "message": "Invalid quantity"}

        totalGain = item.price * quantity

        if shopRepo.getPlayerItemQuantity(playerId, item.name) < quantity:
            return {"success": False, "message": "Not enough items"}

        # APPLY CHANGES VIA REPO
        shopRepo.removePlayerItem(playerId, item.name, quantity)
        shopRepo.increaseStock(item.name, quantity)

        player.gold += totalGain

        return {"success": True, "message": "Sale Successful"}