import random

class LootService:
    def generateLoot(self, enemy):
        name = enemy.name.lower()

        if name == "goblin":
            pool = ["potion", "garbage"]
        elif name == "slime":
            pool = ["potion", "garbage"]
        elif name == "orc":
            pool = ["sword", "potion"]
        elif name == "training dummy":
            pool = ["garbage"]
        else:
            pool = ["potion"]

        inventoryDict = {}

        dropCount = random.randint(0, 2)

        for _ in range(dropCount):
            item = random.choice(pool)
            inventoryDict[item] = inventoryDict.get(item, 0) + 1

        loot = []

        for itemName, qty in inventoryDict.items():
            loot.append({
                "itemName": itemName,
                "qty": qty
            })

        return loot