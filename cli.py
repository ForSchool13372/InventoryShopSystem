#Imports
from controller import Controller
from characterSelectService import selectCharacter
from menuService import MenuService
from shopRepository import ShopRepository
from inventoryRepository import InventoryRepository

#Command Line Interface
class GameCLI:
    def __init__(self, playerId):
        self.controller = Controller(playerId)

        self.menuService = MenuService(ShopRepository())
        self.inventoryRepo = InventoryRepository()

        self.isRunning = True

        self.commands = {
            "1": self.handleBuy,
            "2": self.handleSell,
            "3": self.handleInventory,
            "4": self.handleStats,
            "5": self.handleFight,
            "6": self.handleExit,
            "7": self.handleQuest,
        }

    # ---------------- MAIN LOOP ----------------
    def run(self):
        while self.isRunning:
            print("\n[ GOLD:", self.controller.player.gold,
                  "| HP:", self.controller.player.hp,
                  "| Level:", self.controller.player.level, "]")

            print("-" * 35)
            print("1) Buy        2) Sell")
            print("3) Inventory  4) Stats")
            print("5) Fight      6) Exit")
            print("7) Quest")
            print("-" * 35)

            choice = self.menuService.getChoice()
            command = self.commands.get(choice)

            if command:
                command()
                self.controller.persist()
            else:
                print("Invalid Choice")

    # ---------------- HANDLERS ----------------
    def handleBuy(self):
        itemName, quantity = self.menuService.getBuyFlow()
        result = self.controller.buy(itemName, quantity)
        print(result)

    def handleSell(self):
        items = self.inventoryRepo.loadInventory(self.controller.playerId)
        self.menuService.showInventory(items)

        itemName, quantity = self.menuService.getSellFlow()
        result = self.controller.sell(itemName, quantity)
        print(result)

    def handleInventory(self):
        items = self.controller.getInventory()
        self.menuService.showInventory(items)

    def handleStats(self):
        print("\n--- PLAYER STATS ---")
        print("Gold:", self.controller.player.gold)
        print("HP:", self.controller.player.hp)
        print("Level:", self.controller.player.level)
        print("XP:", self.controller.player.xp)

    def handleFight(self):
        result = self.controller.combatService.handleFight(
            self.controller.player,
            self.controller.enemies
        )

        print(result)

        if result["result"] == "lose":
            self.controller.handleDeath()

        self.controller.persist()

    def handleQuest(self):
        for quest in self.controller.quests:
            if quest.unlocked:
                quest.showQuest()
            else:
                print("\nQuest: ??? (Locked)")

    def handleExit(self):
        self.isRunning = False
        print("Exiting game...")


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    playerId = selectCharacter()
    game = GameCLI(playerId)
    game.run()