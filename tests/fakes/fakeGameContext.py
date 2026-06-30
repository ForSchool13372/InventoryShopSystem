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


class FakeQuestManager:
    def __init__(self):
        self.quests = []
        self.updated_enemy = None

    def update(self, enemy):
        self.updated_enemy = enemy


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


class FakeQuestRepo:
    def saveQuests(self, playerId, quests):
        self.saved = (playerId, quests)


class FakeCtx:
    def __init__(self, fake_shop_repo, fake_quest_manager):

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
            inventory=object(),
            shop=fake_shop_repo,
            quest=FakeQuestRepo()
        )

        self.world = object()

        # IMPORTANT FIX: ensure quests exists
        self.questManager = fake_quest_manager or FakeQuestManager()

        self.gameEventService = FakeEventService()