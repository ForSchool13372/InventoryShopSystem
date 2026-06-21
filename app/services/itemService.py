from app.core.seed import createItems

class ItemService:
    def __init__(self):
        items = createItems()
        self.items = {
            item["itemName"].strip().lower(): item
            for item in items
        }

    def getItem(self, itemName):
        print("LOOKUP:", itemName)
        print("AVAILABLE:", self.items.keys())
        item = self.items.get(itemName.strip().lower())
        print("RESULT:", item)
        return item