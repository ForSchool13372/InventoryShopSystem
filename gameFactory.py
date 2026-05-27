from shopService import ShopService
from shopRepository import ShopRepository
from inventoryRepository import InventoryRepository
from itemService import ItemService
from combatService import CombatService
from gameData import createEnemies, createQuests
from playerRepository import PlayerRepository

from controller import Controller
from gameContext import GameContext


# =========================================================
# DEPENDENCY GROUPS
# =========================================================

class Services:
    def __init__(self, shopService, combatService, itemService):
        self.shop = shopService
        self.combat = combatService
        self.item = itemService


class Repos:
    def __init__(self, shopRepo, inventoryRepo, playerRepo):
        self.shop = shopRepo
        self.inventory = inventoryRepo
        self.player = playerRepo


class World:
    def __init__(self, enemies, quests):
        self.enemies = enemies
        self.quests = quests


# =========================================================
# GAME FACTORY
# =========================================================

class GameFactory:
    def __init__(self):
        # SERVICES
        self.services = Services(
            shopService=ShopService(),
            combatService=CombatService(),
            itemService=ItemService()
        )

        # REPOS
        self.repos = Repos(
            shopRepo=ShopRepository(),
            inventoryRepo=InventoryRepository(),
            playerRepo=PlayerRepository()
        )

        # WORLD (static game data)
        self.world = World(
            enemies=createEnemies(),
            quests=createQuests()
        )

    def create(self, playerId):

        # =====================================================
        # LOAD PLAYER
        # =====================================================
        data = self.repos.player.load(playerId)
        if not data:
            raise ValueError("Player not found")

        from player import Player
        from questManager import QuestManager
        from gameEventService import GameEventService

        player = Player(data["gold"])
        player.hp = data["hp"]
        player.level = data["level"]
        player.xp = data["xp"]

        # =====================================================
        # BUILD DOMAIN SYSTEMS
        # =====================================================
        questManager = QuestManager(self.world.quests, player)
        gameEventService = GameEventService(player, questManager)

        # =====================================================
        # BUILD CONTEXT
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
        # RETURN CONTROLLER
        # =====================================================
        return Controller(ctx)