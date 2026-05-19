from player import Player
from questManager import QuestManager
from combatService import CombatService
from shopService import ShopService
from gameEventService import GameEventService
from itemService import ItemService
from shopRepository import ShopRepository
from inventoryRepository import InventoryRepository
from gameData import createEnemies, createQuests
from database import engine, loadPlayer, savePlayer


class Controller:
    def __init__(self, playerId):
        with engine.begin() as conn:
            data = loadPlayer(conn, playerId)

        self.playerId = playerId

        self.player = Player(data["gold"])
        self.player.hp = data["hp"]
        self.player.level = data["level"]
        self.player.xp = data["xp"]

        self.enemies = createEnemies()
        self.quests = createQuests()

        self.questManager = QuestManager(self.quests, self.player)
        self.gameEventService = GameEventService(self.player, self.questManager)

        self.combatService = CombatService()
        self.shopService = ShopService()

        self.shopRepo = ShopRepository()
        self.inventoryRepo = InventoryRepository()
        self.itemService = ItemService()

    # ---------------- CORE GAME ACTIONS ----------------

    def getInventory(self):
        return self.inventoryRepo.loadInventory(self.playerId)

    def getItem(self, itemName):
        return self.itemService.getItem(itemName)

    def buy(self, itemName, quantity):
        item = self.getItem(itemName.lower())

        return self.shopService.buy(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    def sell(self, itemName, quantity):
        item = self.getItem(itemName.lower())

        return self.shopService.sell(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    def fight(self):
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

        return result

    def getPlayerStats(self):
        return {
            "gold": self.player.gold,
            "hp": self.player.hp,
            "level": self.player.level,
            "xp": self.player.xp
        }

    def getQuests(self):
        return self.quests

    # ---------------- SYSTEM ----------------

    def emitEvent(self, event):
        self.gameEventService.handleEvent(event)

    def revive(self):
        self.player.revive()

    def persist(self):
        with engine.begin() as conn:
            savePlayer(conn, self.player, self.playerId)