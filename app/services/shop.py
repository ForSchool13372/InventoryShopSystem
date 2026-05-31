from app.models.item import Item

class Shop:
    def __init__(self):
        self.stock = {}

    def addItemToStock(self, item, quantity):
        name = getattr(item, "name", item)
        self.stock[name] = self.stock.get(name, 0) + quantity

    def showStock(self):
        for name, qty in self.stock.items():
            print(name, "x", qty)

    def toDict(self):
        return {
            "stock": self.stock
            }

    def fromDict(self, data):
        self.stock = data.get("stock", {})