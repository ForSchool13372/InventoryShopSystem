from app.models.item import Item

class Shop:
    def __init__(self):
        self.stock = {}

    def addItemToStock(self, item, quantity):
        self.stock[item.name] = self.stock.get(item.name, 0) + quantity

    def showStock(self):
        for name, qty in self.stock.items():
            print(name, "x", qty)

    def toDict(self):
        return {
            "stock": self.stock
            }

    def fromDict(self, data):
        self.stock = data.get("stock", {})