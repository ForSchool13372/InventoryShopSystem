from app.services.shopService import ShopService
from app.repositories.shopRepository import ShopRepository
from app.repositories.inventoryRepository import InventoryRepository
from app.services.itemService import ItemService
from app.services.combatService import CombatService
from app.core.gameData import createEnemies, createQuests
from app.repositories.playerRepository import PlayerRepository
from app.core.gameContext import GameContext


# =========================================================
# COMPOSITION ROOT (SHARED SINGLETON-LIKE SYSTEMS)
# =========================================================

class Services:
    def __init__(self):
        self.shop = ShopService()
        self.combat = CombatService()
        self.item = ItemService()


class Repos:
    def __init__(self):
        self.shop = ShopRepository()
        self.inventory = InventoryRepository()
        self.player = PlayerRepository()


class World:
    def __init__(self):
        self.enemies = createEnemies()
        self.quests = createQuests()


# =========================================================
# GAME FACTORY (REQUEST SCOPED CONTEXT BUILDER)
# =========================================================

class GameFactory:
    def __init__(self):
        self.services = Services()
        self.repos = Repos()
        self.world = World()

    def create(self, playerId: int):
        from app.models.player import Player
        from app.core.questManager import QuestManager
        from app.services.gameEventService import GameEventService
        from app.core.controller import Controller

        # -----------------------------------------------------
        # SAFE TYPE
        # -----------------------------------------------------
        playerId = int(playerId)

        # -----------------------------------------------------
        # LOAD PLAYER FROM DB (SOURCE OF TRUTH)
        # -----------------------------------------------------
        data = self.repos.player.load(playerId)

        if not data:
            raise ValueError(f"Player not found: {playerId}")

        # -----------------------------------------------------
        # BUILD PLAYER OBJECT (TEMP RUNTIME MODEL ONLY)
        # -----------------------------------------------------
        player = Player(
            gold=data.get("gold", 0)
        )
        player.hp = data.get("hp", 100)
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)

        # -----------------------------------------------------
        # GAME SYSTEMS (SCOPED PER REQUEST)
        # -----------------------------------------------------
        questManager = QuestManager(self.world.quests, player)
        gameEventService = GameEventService(player, questManager)

        # -----------------------------------------------------
        # CONTEXT
        # -----------------------------------------------------
        ctx = GameContext(
            player=player,
            playerId=playerId,
            services=self.services,
            repos=self.repos,
            world=self.world,
            questManager=questManager,
            gameEventService=gameEventService
        )

        return Controller(ctx)