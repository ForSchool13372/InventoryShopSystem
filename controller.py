from player import Player
from combatService import CombatService
from auth import createAccessToken
from playerRepository import PlayerRepository
from questManager import QuestManager
from gameEventService import GameEventService


class Controller:
    def __init__(
        self,
        playerId,
        shopService,
        shopRepo,
        inventoryRepo,
        itemService,
        combatService,
        enemies,
        quests
    ):
        # ---------------- REPOSITORY ----------------
        self.playerRepo = PlayerRepository()

        data = self.playerRepo.load(playerId)
        if not data:
            raise ValueError("Player not found")

        # ---------------- PLAYER STATE ----------------
        self.playerId = playerId
        self.player = Player(data["gold"])
        self.player.hp = data["hp"]
        self.player.level = data["level"]
        self.player.xp = data["xp"]

        # ---------------- DOMAIN STATE (INJECTED) ----------------
        # Important: Controller does NOT construct game world
        self.enemies = enemies
        self.quests = quests

        # ---------------- SYSTEMS ----------------
        self.questManager = QuestManager(self.quests, self.player)
        self.gameEventService = GameEventService(self.player, self.questManager)

        # ---------------- SERVICES ----------------
        self.combatService = combatService
        self.shopService = shopService
        self.shopRepo = shopRepo
        self.inventoryRepo = inventoryRepo
        self.itemService = itemService

    # =========================================================
    # AUTH / LIFECYCLE
    # =========================================================

    def login(self):
        return {
            "success": True,
            "token": createAccessToken({"playerId": self.playerId})
        }

    def revive(self):
        self.player.revive()

    def persist(self):
        self.playerRepo.save(self.playerId, self.player)

    # =========================================================
    # PLAYER INFO
    # =========================================================

    def getPlayerStats(self):
        return {
            "gold": self.player.gold,
            "hp": self.player.hp,
            "level": self.player.level,
            "xp": self.player.xp
        }

    # =========================================================
    # GAME ACTIONS (ORCHESTRATION ONLY)
    # =========================================================

    def fight(self):
        result = self.combatService.handleFight(self.player, self.enemies)

        if result["result"] == "win":
            self.emitEvent({
                "type": "fightWin",
                "xp": result["xp"],
                "enemy": result["enemy"]
            })
        else:
            self.emitEvent({"type": "fightLose"})

        return result

    def buy(self, itemName, quantity):
        item = self.itemService.getItem(itemName.lower())

        return self.shopService.buy(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    def sell(self, itemName, quantity):
        item = self.itemService.getItem(itemName.lower())

        return self.shopService.sell(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    # =========================================================
    # DATA ACCESS
    # =========================================================

    def getShop(self):
        return self.shopRepo.getShopItems()

    def getInventory(self):
        return self.inventoryRepo.loadInventory(self.playerId)

    def getQuests(self):
        return self.quests

    # =========================================================
    # INTERNAL EVENTS
    # =========================================================

    def emitEvent(self, event):
        self.gameEventService.handleEvent(event)