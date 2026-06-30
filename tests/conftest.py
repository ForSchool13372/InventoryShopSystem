import pytest
import app.core.redisClient as redisModule
from tests.fakes.fakeRedis import FakeRedis
from app.core.game.controller import Controller
from app.core.database import Base, engine

from fastapi.testclient import TestClient
from app.main import app

from app.models.item import Item
from app.models.player import Player
from app.models.enemy import Enemy

from tests.fakes.fakeGameContext import FakeCtx, FakeQuestManager


# =========================================================
# GLOBAL MOCKS (AUTOUSE FIXTURES)
# =========================================================

@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(redisModule, "redisClient", fake)
    return fake

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    from app.core.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# =========================================================
# API TEST CLIENT FIXTURES
# =========================================================

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def ws_client(client):
    return client.websocket_connect


# =========================================================
# AUTH FIXTURES
# =========================================================

@pytest.fixture
def token(client):
    response = client.post("/api/login", json={"playerId": 1})
    data = response.json()

    assert "token" in data
    return data["token"]


# =========================================================
# FACTORY HELPERS
# =========================================================

@pytest.fixture
def create_item():
    def _create(name="sword", price=10):
        return Item(name, price)
    return _create


@pytest.fixture
def create_player():
    def _create(gold=100):
        return Player(gold)
    return _create


@pytest.fixture
def create_enemy():
    def _create():
        return Enemy(
            name="goblin",
            hp=30,
            xp=10,
            minDamage=1,
            maxDamage=5
        )
    return _create


# =========================================================
# SIMPLE REPO FAKE (ONLY USED HERE)
# =========================================================

class FakeShopRepo:
    def __init__(self):
        self.stock = {"sword": 10, "potion": 10}
        self.playerItems = {}

    def getStock(self, conn, itemName):
        if itemName not in self.stock:
            return None
        return {"stock": self.stock[itemName]}

    def decreaseStock(self, conn, itemName, quantity):
        self.stock[itemName] -= quantity

    def increaseStock(self, conn, itemName, quantity):
        self.stock[itemName] = self.stock.get(itemName, 0) + quantity

    def addOrUpdatePlayerItem(self, conn, playerId, itemName, quantity):
        self.playerItems[itemName] = self.playerItems.get(itemName, 0) + quantity

    def removePlayerItem(self, conn, playerId, itemName, quantity):
        if itemName in self.playerItems:
            self.playerItems[itemName] -= quantity
            if self.playerItems[itemName] <= 0:
                del self.playerItems[itemName]

    def getPlayerItemQuantity(self, conn, playerId, itemName):
        if itemName not in self.playerItems:
            return {"quantity": 0}
        return {"quantity": self.playerItems[itemName]}


@pytest.fixture
def fake_shop_repo():
    return FakeShopRepo()


# =========================================================
# QUEST FIXTURE (MUST BE BEFORE CONTROLLER)
# =========================================================

@pytest.fixture
def fake_quest_manager():
    return FakeQuestManager()


# =========================================================
# CONTROLLER FIXTURE (NOW CLEAN)
# =========================================================

@pytest.fixture
def controller(fake_shop_repo, fake_quest_manager):
    ctx = FakeCtx(fake_shop_repo, fake_quest_manager)
    return Controller(ctx)