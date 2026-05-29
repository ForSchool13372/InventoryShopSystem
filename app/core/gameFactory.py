from app.services.shopService import ShopService
from app.repositories.shopRepository import ShopRepository
from app.repositories.inventoryRepository import InventoryRepository
from app.services.itemService import ItemService
from app.services.combatService import CombatService
from app.core.gameData import createEnemies, createQuests
from app.repositories.playerRepository import PlayerRepository

from app.core.gameContext import GameContext

# =========================================================
# CORE GROUPS
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
# GAME FACTORY (COMPOSITION ROOT)
# =========================================================

class GameFactory:
    def __init__(self):
        self.services = Services()
        self.repos = Repos()
        self.world = World()

    def create(self, playerId):

        # =====================================================
        # LOAD PLAYER
        # =====================================================
        data = self.repos.player.load(playerId)
        if not data:
            raise ValueError("Player not found")

        from app.models.player import Player
        from app.core.questManager import QuestManager
        from app.services.gameEventService import GameEventService
        from app.core.controller import Controller

        player = Player(data["gold"])
        player.hp = data["hp"]
        player.level = data["level"]
        player.xp = data["xp"]

        # =====================================================
        # DOMAIN SYSTEMS (NOT FACTORY RESPONSIBILITY LONG TERM)
        # =====================================================
        questManager = QuestManager(self.world.quests, player)
        gameEventService = GameEventService(player, questManager)

        # =====================================================
        # CONTEXT
        # =====================================================
        ctx = GameContext(
            player=player,
            playerId=playerId,
            services=self.services,
            repos=self.repos,
            world=self.world,
            questManager=questManager,
            gameEventService=gameEventService
        )

        # =====================================================
        # CONTROLLER
        # =====================================================
        return Controller(ctx)