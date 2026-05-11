from item import Item

class Shop:
    def __init__(self):
        self.stock = {}

    def addItemToStock(self, item, quantity):
        self.stock[item.name] = self.stock.get(item.name, 0) + quantity

    def buyItem(self, player, item, quantity):
        totalCost = item.price * quantity

        if self.stock.get(item.name, 0) < quantity:
            print("Not enough stock")
            return False

        if player.gold < totalCost:
            print("Not enough gold")
            return False

        player.gold -= totalCost

        for _ in range(quantity):
            player.inventory.addItem(item)

        self.stock[item.name] -= quantity

        return True

    def sellItem(self, player, item, quantity):
        if quantity <= 0:
            print("Invalid quantity")
            return False

        if not item:
            print("Item does not exist")
            return False

        if player.inventory.items.get(item.name, 0) < quantity:
            print("Not enough items to sell")
            return False

        totalGain = item.price * quantity
        player.gold += totalGain

        for _ in range(quantity):
            player.inventory.removeItem(item)

        self.stock[item.name] = self.stock.get(item.name, 0) + quantity

        return True

    def showStock(self):
        for name, qty in self.stock.items():
            print(name, "x", qty)