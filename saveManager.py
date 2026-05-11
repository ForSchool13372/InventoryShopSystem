import json

class SaveManager:
    def loadgame(self, player, shop):
        try:
            with open("save.json", "r") as file:
                data = json.load(file)

            player.gold = data.get("gold", 0)
            player.level = data.get("level", 1)
            player.xp = data.get("xp", 0)
            player.hp = data.get("hp", 100)

            player.inventory.items.clear()
            for name, qty in data.get("inventory", {}).items():
                player.inventory.items[name] = qty

            shop.stock.clear()
            shop.stock.update(data.get("stock", {}))

            print("Game loaded")
            return True

        except FileNotFoundError:
            print("No save file found")
            return False

    def saveGame(self, player, shop):
        data = {
            "gold": player.gold,
            "inventory": player.inventory.items,
            "stock": shop.stock,
            "level": player.level,
            "xp": player.xp,
            "hp": player.hp
            }

        with open("save.json", "w") as file:
            json.dump(data,file)
