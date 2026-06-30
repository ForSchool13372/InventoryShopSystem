class InventoryService:
    def __init__(self, inventoryRepo):
        self.inventoryRepo = inventoryRepo

    def addItems(self, playerId: int, items: list):
        if not items:
            return

        currentInventory = self.inventoryRepo.loadInventory(playerId)

        inventoryDict = {
            item["itemName"]: item["quantity"]
            for item in currentInventory
        }

        for item in items:
            name = item["itemName"]
            qty = item.get("qty", 1)

            inventoryDict[name] = inventoryDict.get(name, 0) + qty

        self.inventoryRepo.saveInventory(playerId, inventoryDict)