from app.services.shopService import ShopService
from app.repositories.shopRepository import ShopRepository
from app.services.inventoryService import InventoryService
from app.repositories.inventoryRepository import InventoryRepository
from app.services.itemService import ItemService
from app.services.combatService import CombatService
from app.services.leaderboardService import LeaderboardService
from app.core.game.seed import createEnemies, createQuests
from app.repositories.playerRepository import PlayerRepository
from app.core.game.gameContext import GameContext
from app.state.gameState import gameState
from app.repositories.questRepository import QuestRepository
from app.services.lootService import LootService
from app.models.quest import Quest


# =========================================================
# COMPOSITION ROOT
# =========================================================

class Services:
    def __init__(self, repos):
        self.shop = ShopService(repos.shop)
        self.combat = CombatService()
        self.item = ItemService()
        self.leaderboard = LeaderboardService(repos.player)
        self.loot = LootService()
        self.inventory = InventoryService(repos.inventory)


class Repos:
    def __init__(self):
        self.shop = ShopRepository()
        self.inventory = InventoryRepository()
        self.player = PlayerRepository()
        self.quest = QuestRepository()


class World:
    def __init__(self):
        self.enemies = createEnemies()
        self.quests = createQuests()


class PlayerFactory:
    @staticmethod
    def fromData(playerId: int, data: dict):
        from app.models.player import Player

        player = Player(
            playerId=playerId,
            gold=data.get("gold", 0),
            hp=data.get("hp", 100),
            maxhp=data.get("maxhp", 100),
            level=data.get("level", 1),
            xp=data.get("xp", 0)
        )

        player.combat["attack"] = data.get("attack", 10)
        player.combat["defense"] = data.get("defense", 5)
        player.combat["critchance"] = data.get("critchance", 0.05)
        player.combat["critmultiplier"] = data.get("critmultiplier", 1.5)

        return player


class GameFactory:
    def __init__(self):
        self.repos = Repos()
        self.services = Services(self.repos)
        self.world = World()

    def create(self, playerId: int):
        from app.core.game.questManager import QuestManager
        from app.services.gameEventService import GameEventService
        from app.core.game.controller import Controller
        from app.core.wsManager import wsManager  

        playerId = int(playerId)

        # =========================
        # PLAYER LOAD
        # =========================
        player = gameState.getPlayer(playerId)

        if player is None:
            data = self.repos.player.load(playerId)

            if not data:
                raise ValueError(f"Player not found: {playerId}")

            player = PlayerFactory.fromData(playerId, data)
            gameState.addPlayer(playerId, player)

        # =========================
        # QUEST LOAD
        # =========================
        questData = self.repos.quest.loadQuests(playerId) or []

        quests = [
            Quest(
                name=q["name"],
                targetEnemy=q["targetenemy"],
                target=q["target"],
                rewardXP=q["rewardxp"],
                rewardGold=q["rewardgold"],
                progress=q["progress"],
                completed=q["completed"],
                unlocked=q["unlocked"],
                claimed=q["claimed"]
            )
            for q in questData
        ]

        questManager = QuestManager(quests, player, self.repos.quest)

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
    # LB Access
    # =========================

    def getLeaderboard(self):
        return gameState.getLeaderboard()