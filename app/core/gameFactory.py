from app.services.shopService import ShopService
from app.repositories.shopRepository import ShopRepository
from app.repositories.inventoryRepository import InventoryRepository
from app.services.itemService import ItemService
from app.services.combatService import CombatService
from app.services.leaderboardService import LeaderboardService
from app.core.seed import createEnemies, createQuests
from app.repositories.playerRepository import PlayerRepository
from app.core.gameContext import GameContext
from app.state.gameState import gameState


# =========================================================
# COMPOSITION ROOT
# =========================================================

class Services:
    def __init__(self, repos):
        self.shop = ShopService(repos.shop)
        self.combat = CombatService()
        self.item = ItemService()
        self.leaderboard = LeaderboardService(repos.player)


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
# PLAYER FACTORY (DOMAIN HYDRATION)
# =========================================================

class PlayerFactory:
    @staticmethod
    def fromData(data):
        from app.models.player import Player

        player = Player(
            gold=data.get("gold", 0),
            hp=data.get("hp", 100),
            maxHp=data.get("maxhp", 100),
            level=data.get("level", 1),
            xp=data.get("xp", 0)
        )

        player.combat["attack"] = data.get("attack", player.combat["attack"])
        player.combat["defense"] = data.get("defense", player.combat["defense"])
        player.combat["critChance"] = data.get("critchance", player.combat["critChance"])
        player.combat["critMultiplier"] = data.get("critmultiplier", player.combat["critMultiplier"])

        return player


# =========================================================
# GAME FACTORY (COMPOSITION ROOT ONLY)
# =========================================================

class GameFactory:
    def __init__(self):
        self.repos = Repos()
        self.services = Services(self.repos)
        self.world = World()

    def create(self, playerId: int):
        from app.core.questManager import QuestManager
        from app.services.gameEventService import GameEventService
        from app.core.controller import Controller
        from app.core.wsManager import wsManager  

        playerId = int(playerId)

        # =========================
        # ALWAYS SINGLE SOURCE OF TRUTH
        # =========================
        player = gameState.getPlayer(playerId)

        if player is None:
            data = self.repos.player.load(playerId)

            if not data:
                raise ValueError(f"Player not found: {playerId}")

            player = PlayerFactory.fromData(data)
            gameState.addPlayer(playerId, player)

        questManager = QuestManager(self.world.quests, player)

        gameEventService = GameEventService(
            gameState,
            questManager,
            wsManager
        )

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

    # =========================
    # LEADERBOARD ACCESS
    # =========================
    def getLeaderboard(self):
        return gameState.getLeaderboard()