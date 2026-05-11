class ShopService:
    def __init__(self, shop):
        self.shop = shop

    def buy(self, player, item, quantity):
        # 1. Check item exists
        if not item:
            print("Item does not exist")
            return False

        # 2. Check stock
        if self.shop.stock.get(item.name, 0) < quantity:
            print("Not enough stock")
            return False

        # 3. Calculate cost
        totalCost = item.price * quantity

        # 4. Check gold
        if player.gold < totalCost:
            print("Not Enough gold")
            return False

        # 5. Apply Transaction
        player.gold -= totalCost
        self.shop.stock[item.name] -= quantity

        for _ in range(quantity):
            player.inventory.addItem(item)

        return True

    def sell(self, player, item, quantity):
        # 1. Check if item exist
        if not item:
            print("Item does not exist")
            return False

        # 2. Check quantity is valid
        if quantity <= 0:
            print("Invalid quantity")
            return False

        # 3. Check if player has item
        if player.inventory.items.get(item.name, 0) < quantity:
            print("Not enough items")
            return False

        # 4. Calculate gain
        totalGain = item.price * quantity

        # 5. Apply transaction
        player.gold += totalGain

        for _ in range(quantity):
            player.inventory.removeItem(item)

        self.shop.stock[item.name] = self.shop.stock.get(item.name, 0) + quantity

        return True

    def addStock(self, item, quantity):
        self.shop.addItemToStock(item, quantity)