#Imports (Tools)
from player import Player
from item import Item
from enemy import Enemy
from shop import Shop
from quest import Quest
from questManager import QuestManager
from saveManager import SaveManager
from inputHandler import InputHandler
from combatService import CombatService
from shopService import ShopService
from gameEventService import GameEventService
from menuService import MenuService
from itemService import ItemService
from gameData import createEnemies,createItems,createQuests, seedShop

class Controller:
    def __init__(self):
        self.player = Player(100)
        self.shop = Shop()
        self.isRunning = True
        self.enemies = createEnemies()
        self.quests = createQuests()
        self.questManager = QuestManager(self.quests, self.player)
        self.gameEventService = GameEventService(self.player, self.questManager)
        self.saveManager = SaveManager()
        self.inputHandler = InputHandler()
        self.combatService = CombatService()
        self.shopService = ShopService(self.shop)
        self.menuService = MenuService(self)
        self.itemService = ItemService()
        
        loaded = self.saveManager.loadgame(self.player, self.shop)

        if not loaded:
            seedShop(self.shop)

    #Event Handlers
    def handleInventory(self):
        self.player.inventory.showInventory()

    def handleBuy(self):
        self.shop.showStock()
        itemName = self.inputHandler.getInput("Enter item name: ").lower()

        try:
            quantity = int(self.inputHandler.getInput("Enter quantity: "))
        except ValueError:
            print("Invalid Quantity")
            return 

        self.buy(itemName, quantity)

    def handleSell(self):
        self.player.inventory.showInventory()
        itemName = self.inputHandler.getInput("Enter item name: ").strip().lower()

        try:
            quantity = int(self.inputHandler.getInput("Enter quantity: "))
        except ValueError:
            print("Invalid quantity")
            return

        self.sell(itemName, quantity)

    def handleStats(self):
        self.player.showStats()

    def handleDeath(self):
        print("\nGame Over")

        while True:
            choice = self.inputHandler.getInput("Revive? (y/n): ").lower()

            if choice == "y":
                self.revive()
                break
            elif choice == "n":
                self.isRunning = False
                break
            else:
                print("Invalid input, try again")

    def handleFight(self):
        result = self.combatService.handleFight(self.player, self.enemies)

        if result["result"] == "win":
            self.emitEvent({
                "type": "fightWin",
                "xp": result["xp"],
                "enemy": result["enemy"]
                })
        else:
            self.emitEvent({
                "type": "fightLose"
                })

    def handleSave(self):
        self.saveGame()
        print("Game Saved")

    def handleExit(self):
        self.isRunning = False
        print("Exiting game...")

    def handleQuest(self):
        for quest in self.quests:
            if quest.unlocked:
                quest.showQuest()
            else:
                print("\nQuest: ??? (Locked)")

    def emitEvent(self, event):
        self.gameEventService.handleEvent(event)

    #Revive method
    def revive(self):
        self.player.revive()
        self.isRunning = True

    def getItem(self, itemName):
        return self.itemService.getItem(itemName)

    def getInventory(self):
        return self.player.inventory.items

    def saveGame(self):
        self.saveManager.saveGame(self.player, self.shop)
    
    def buy(self, itemName, quantity):
        itemName = itemName.lower()
        item = self.getItem(itemName)
        return self.shopService.buy(self.player, item, quantity)

    def sell(self, itemName, quantity):
        itemName = itemName.lower()
        item = self.getItem(itemName)

        return self.shopService.sell(self.player, item, quantity)

    def run(self):
        actions = self.menuService.getActions()

        while self.isRunning:
            print("\n[ GOLD:", self.player.gold, "| HP:", self.player.hp,f"| Level: {self.player.level} ]")
            print("-"*35)
            print("1) Buy        2) Sell")
            print("3) Inventory  4) Stats")
            print("5) Fight      6) Exit")
            print("7) Save       8) Quests")
            print("-"*35)
            choice = self.inputHandler.getInput("> ")

            action = actions.get(choice)

            if action:
                action()
            else:
                print("Invalid Choice")

#Main
if __name__ == "__main__":
    game = Controller()
    game.run()