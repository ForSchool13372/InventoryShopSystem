class Inventory:
    def __init__(self):
        self.items = {}

    def addItem(self, item):
        if item.name in self.items:
            self.items[item.name] += 1 #Increases the count if already owned
        else:
            self.items[item.name] = 1 #Start at 1 if not owned

    def showInventory(self):
        for name, qty in self.items.items():
            print(name, "x", qty)

    def removeItem(self, item):
        if item.name in self.items:
            self.items[item.name] -= 1

            if self.items[item.name] <= 0:
                del self.items[item.name]

    def fromDict(self, data):
        self.items = data

    def toDict(self):
        return self.items