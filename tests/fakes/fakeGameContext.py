from types import SimpleNamespace
from tests.fakes.gameFakes import (
    FakeCombat,
    FakeShop,
    FakeItemService,
    FakeLoot,
    FakeInventory,
    FakeLeaderboard,
    FakeEventService
)


# =========================================================
# QUEST MANAGER (FIXED)
# =========================================================

class FakeQuestManager:
    def __init__(self):
        self.quests = []
        self.updated_enemy = None

    def update(self, enemy):
        self.updated_enemy = enemy

    def claimQuest(self, quest):
        # Controller expects xp + gold
        quest.completed = True
        quest.claimed = True

        return {
            "xp": 10,
            "gold": 5
        }


# =========================================================
# PLAYER REPO
# =========================================================

class FakePlayerRepoSimple:
    def load(self, playerId):
        return {
            "gold": 100,
            "hp": 100,
            "maxhp": 100,
            "level": 1,
            "xp": 0,
            "attack": 10,
            "defense": 5,
            "critchance": 0.05,
            "critmultiplier": 1.5,
        }

    def save(self, playerId, player):
        pass


# =========================================================
# QUEST REPO
# =========================================================

class FakeQuestRepo:
    def __init__(self):
        self.saved = None

    def saveQuests(self, playerId, quests):
        self.saved = (playerId, quests)


# =========================================================
# SHOP REPO (FIXED)
# =========================================================

class FakeShopRepo:
    def __init__(self):
        self.stock = {"sword": 10, "potion": 5}

    def getShopStock(self):
        return self.stock


# =========================================================
# INVENTORY REPO (FIXED)
# =========================================================

class FakeInventoryRepo:
    def loadInventory(self, playerId):
        return {
            "items": []
        }


# =========================================================
# CONTEXT
# =========================================================

class FakeCtx:
    def __init__(self, fake_shop_repo=None, fake_quest_manager=None):

        self.playerId = 1
        self.playerRepo = FakePlayerRepoSimple()

        self.services = SimpleNamespace(
            combat=FakeCombat(),
            shop=FakeShop(),
            item=FakeItemService(),
            loot=FakeLoot(),
            inventory=FakeInventory(),
            leaderboard=FakeLeaderboard()
        )

        self.repos = SimpleNamespace(
            player=self.playerRepo,
            inventory=FakeInventoryRepo(),
            shop=FakeShopRepo(),
            quest=FakeQuestRepo()
        )

        self.world = object()

        self.questManager = fake_quest_manager or FakeQuestManager()

        self.gameEventService = FakeEventService()