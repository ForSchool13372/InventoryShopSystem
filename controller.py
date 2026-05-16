#Imports (Tools)
from player import Player
from item import Item
from enemy import Enemy
from quest import Quest
from questManager import QuestManager
from combatService import CombatService
from shopService import ShopService
from gameEventService import GameEventService
from menuService import MenuService
from itemService import ItemService
from gameData import createEnemies,createItems,createQuests, seedShop
from database import engine, loadPlayer, savePlayer
from sqlalchemy import text

class Controller:
    def __init__(self):
        with engine.begin() as conn:
            data = loadPlayer(conn)

        self.player = Player(data["gold"])
        self.player.hp = data["hp"]
        self.player.level = data["level"]
        self.player.xp = data["xp"]
        self.isRunning = True
        self.enemies = createEnemies()
        self.quests = createQuests()
        self.questManager = QuestManager(self.quests, self.player)
        self.gameEventService = GameEventService(self.player, self.questManager)
        self.combatService = CombatService()
        self.shopService = ShopService()
        self.menuService = MenuService(self)
        self.itemService = ItemService()

    #Event Handlers
    def handleInventory(self):
        items = self.getInventory()
        print(items)

    def handleBuy(self, itemName, quantity):
        self.buy(itemName.lower(), quantity)

    def handleSell(self, itemName, quantity):
        self.sell(itemName.lower(), quantity)

    def handleStats(self):
        self.player.showStats()

    def handleDeath(self):
        print("\nGame Over")

        while True:
            choice = input("Revive? (y/n): ").lower()

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

    def persist(self):
        with engine.begin() as conn:
            savePlayer(conn, self.player)

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
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT itemName, quantity
                FROM playerItems
                WHERE playerID = 1
            """)).fetchall()

        return [
            {"itemName": r[0], "quantity": r[1]}
                for r in rows
            ]
    
    def buy(self, itemName, quantity):
        itemName = itemName.lower()
        item = self.getItem(itemName)

        result = self.shopService.buy(self.player, item, quantity)

        if result["success"]:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO playerItems (playerID, itemName, quantity)
                    VALUES (1, :itemName, :qty)
                    ON CONFLICT(playerID, itemName)
                    DO UPDATE SET quantity = quantity + :qty
                """),{
                             "itemName": itemName,
                             "qty": quantity
                })

        return result

    def sell(self, itemName, quantity):
        itemName = itemName.lower()
        item = self.getItem(itemName)

        result = self.shopService.sell(self.player, item, quantity)

        if result["success"]:
            with engine.begin() as conn:
                conn.execute(text("""
                    UPDATE playerItems
                    SET quantity = quantity - :qty
                    WHERE playerID = 1 AND itemName = :itemName
                """),{
                    "itemName": itemName,
                    "qty": quantity
                    })
    
                conn.execute(text("""
                    DELETE FROM playerItems
                    WHERE playerID = 1 AND quantity <= 0
                """))

        return result

    def promptBuy(self):
        return self.menuService.getBuyInput()

    def promptSell(self):
        return self.menuService.getSellInput()

    def run(self):
        actions = self.menuService.getActions()

        while self.isRunning:
            print("\n[ GOLD:", self.player.gold, "| HP:", self.player.hp,f"| Level: {self.player.level} ]")
            print("-"*35)
            print("1) Buy        2) Sell")
            print("3) Inventory  4) Stats")
            print("5) Fight      6) Exit")
            print("7) Quest")
            print("-"*35)
            choice = input("> ")

            action = actions.get(choice)

            if action:
                if choice == "1":
                    with engine.begin() as conn:
                        rows = conn.execute(text("SELECT itemName, stock FROM shop")).fetchall()
                        for r in rows:
                            print(r[0], "x", r[1])
                    self.handleBuy(*self.promptBuy())
                    self.persist()
                elif choice == "2":
                    self.handleSell(*self.promptSell())
                    self.persist()
                else:
                    action()
                    self.persist()
            else:
                print("Invalid Choice")

#Main
if __name__ == "__main__":
    game = Controller()
    game.run()