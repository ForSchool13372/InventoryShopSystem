from app.core.game.seed import createItems

class ItemService:
    def __init__(self):
        items = createItems()

        self.items = {
            (item.get("itemName") or item.get("itemname")).strip().lower(): item
            for item in items
        }

    def getItem(self, itemName):
        print("LOOKUP:", itemName)
        print("AVAILABLE:", self.items.keys())

        key = itemName.strip().lower()
        item = self.items.get(key)

        print("RESULT:", item)
        return item