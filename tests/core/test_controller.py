import pytest

from app.core.controller import Controller
from app.state.gameState import gameState


class FakeEventService:
    def __init__(self):
        self.events = []

    def handleEvent(self, event):
        self.events.append(event)


class FakePlayer:
    def __init__(self):
        self.gold = 100
        self.hp = 50
        self.level = 2
        self.xp = 10

    def revive(self):
        self.hp = 100

    def getStats(self):
        return {
            "gold": self.gold,
            "hp": self.hp,
            "level": self.level,
            "xp": self.xp
        }


class FakeCombat:
    def handleFight(self, player, worldEnemies):
        return {
            "result": "win",
            "xp": 20,
            "enemy": "goblin",
        }


class FakeShop:
    def buy(self, ctx):
        return {"success": True, "action": "buy"}

    def sell(self, ctx):
        return {"success": True, "action": "sell"}


class FakeItemService:
    def getItem(self, name):
        if name == "sword":
            return {"name": "sword"}
        return None


class FakeRepo:
    def __init__(self):
        self.saved = None

    def load(self, playerId):
        return {
            "gold": 100,
            "hp": 50,
            "level": 2,
            "xp": 10
        }

    def save(self, playerId, player):
        self.saved = (playerId, player)

    def getShopStock(self):
        return ["item1"]

    def loadInventory(self, playerId):
        return ["inv1"]


class FakeWorld:
    def __init__(self):
        self.enemies = ["goblin"]


class FakeServices:
    def __init__(self):
        self.combat = FakeCombat()
        self.shop = FakeShop()
        self.item = FakeItemService()


class FakeRepos:
    def __init__(self):
        self.shop = FakeRepo()
        self.inventory = FakeRepo()
        self.player = FakeRepo()


class FakeCtx:
    def __init__(self):
        self.player = FakePlayer()
        self.playerId = 1
        self.services = FakeServices()
        self.repos = FakeRepos()
        self.world = FakeWorld()
        self.world.quests = []
        self.questManager = None
        self.gameEventService = FakeEventService()


def test_login_returns_token_and_emits_event(monkeypatch):
    import app.core.controller as controllerModule

    monkeypatch.setattr(controllerModule, "createAccessToken", lambda payload: "token123")

    ctx = FakeCtx()
    ctrl = Controller(ctx)

    result = ctrl.login()

    assert result["success"] is True
    assert result["id"] == 1
    assert result["token"] == "token123"
    assert ctx.gameEventService.events[0]["type"] == "LOGIN"


def test_revive_restores_hp():
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    # Add player to gameState (Controller expects this)
    gameState.addPlayer(1, ctx.player)

    ctx.player.hp = 10
    result = ctrl.revive()

    assert result["success"] is True
    assert ctx.player.hp == 100


def test_get_player_stats():
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    # Add player to gameState (Controller expects this)
    gameState.addPlayer(1, ctx.player)

    stats = ctrl.getPlayerStats()

    assert stats["gold"] == 100
    assert stats["hp"] == 50
    assert stats["level"] == 2
    assert stats["xp"] == 10


def test_fight_emits_event(monkeypatch):
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    gameState.addPlayer(1, ctx.player)

    result = ctrl.fight()

    assert result["result"] == "win"
    assert ctx.gameEventService.events[0]["type"] == "FIGHT_WIN"


def test_buy_success(monkeypatch):
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    gameState.addPlayer(1, ctx.player)

    result = ctrl.buy("sword", 2)

    assert result["success"] is True
    assert ctx.gameEventService.events[-1]["type"] == "BUY"


def test_buy_item_not_found():
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    gameState.addPlayer(1, ctx.player)

    result = ctrl.buy("invalid", 1)

    assert result["success"] is False
    assert result["message"] == "Item not found"


def test_sell_success():
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    gameState.addPlayer(1, ctx.player)

    result = ctrl.sell("sword", 1)

    assert result["success"] is True
    assert ctx.gameEventService.events[-1]["type"] == "SELL"


def test_data_access_methods():
    ctx = FakeCtx()
    ctrl = Controller(ctx)

    assert ctrl.getShop() == ["item1"]
    assert ctrl.getInventory() == ["inv1"]
    assert ctrl.getQuests() == []
