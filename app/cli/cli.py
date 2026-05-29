#Imports
from app.services.characterSelectService import selectCharacter
from app.services.menuService import MenuService
from app.core.gameFactory import GameFactory


# =========================================================
# CLI
# =========================================================

class GameCLI:
    def __init__(self, playerId):

        # CONTROLLER
        self.gameFactory = GameFactory()
        self.controller = self.gameFactory.create(playerId)

        # MENU
        self.menuService = MenuService(self.controller.shopRepo)

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

    # =========================================================
    # MAIN LOOP
    # =========================================================

    def run(self):
        while self.isRunning:
            self._printHeader()

            choice = self.menuService.getChoice()
            command = self.commands.get(choice)

            if command:
                command()
                self.controller.persist()
            else:
                print("Invalid choice")

    # =========================================================
    # RESULT HANDLER (STANDARDIZED OUTPUT)
    # =========================================================

    def _handleResult(self, result):
        if isinstance(result, dict):
            if result.get("success") is False:
                print(f"[ERROR] {result.get('message')}")
            else:
                print(result.get("message", result))
        else:
            print(result)

    # =========================================================
    # UI HEADER
    # =========================================================

    def _printHeader(self):
        player = self.controller.player

        print("\n[ GOLD:", player.gold,
              "| HP:", player.hp,
              "| Level:", player.level, "]")

        print("-" * 35)
        print("1) Buy        2) Sell")
        print("3) Inventory  4) Stats")
        print("5) Fight      6) Exit")
        print("7) Quest")
        print("-" * 35)

    # =========================================================
    # ACTION HANDLERS
    # =========================================================

    def handleBuy(self):
        try:
            itemName, quantity = self.menuService.getBuyFlow()
            result = self.controller.buy(itemName, quantity)
            self._handleResult(result)
        except Exception as e:
            self._handleResult({"success": False, "message": str(e)})

    def handleSell(self):
        try:
            items = self.controller.getInventory()
            self.menuService.showInventory(items)

            itemName, quantity = self.menuService.getSellFlow()
            result = self.controller.sell(itemName, quantity)
            self._handleResult(result)

        except Exception as e:
            self._handleResult({"success": False, "message": str(e)})

    def handleInventory(self):
        items = self.controller.getInventory()
        self.menuService.showInventory(items)

    def handleStats(self):
        stats = self.controller.getPlayerStats()

        print("\n--- PLAYER STATS ---")
        print("Gold:", stats["gold"])
        print("HP:", stats["hp"])
        print("Level:", stats["level"])
        print("XP:", stats["xp"])

    def handleFight(self):
        result = self.controller.fight()
        self._handleResult(result)

        if isinstance(result, dict) and result.get("result") == "lose":
            self.controller.revive()

    def handleQuest(self):
        quests = self.controller.getQuests()

        for quest in quests:
            if quest.unlocked:
                quest.showQuest()
            else:
                print("\nQuest: ??? (Locked)")

    def handleExit(self):
        self.isRunning = False
        print("Exiting game...")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    playerId = selectCharacter()
    game = GameCLI(playerId)
    game.run()