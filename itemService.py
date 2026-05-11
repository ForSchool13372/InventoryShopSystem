from gameData import createItems

class ItemService:
    def __init__(self):
        self.items = createItems()

    def getItem(self, itemName):
        return self.items.get(itemName.lower())