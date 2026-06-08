import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.item import Item
from app.models.player import Player
from app.models.enemy import Enemy


# =========================================================
# CLIENT FIXTURE
# =========================================================

@pytest.fixture
def client():
    return TestClient(app)


# =========================================================
# AUTH FIXTURE
# =========================================================

@pytest.fixture
def token(client):
    response = client.post("/api/login", json={"playerId": 1})

    data = response.json()
    assert "token" in data

    return data["token"]


# =========================================================
# FACTORIES
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
# FAKE ENGINE (IMPORTANT FIX)
# =========================================================

class FakeResult:
    def __init__(self, row=None, rows=None):
        self._row = row
        self._rows = rows or []

    def fetchone(self):
        return self._row

    def fetchall(self):
        return self._rows


class FakeConn:
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((str(query), params))

        q = str(query)

        if "SELECT stock" in q:
            return FakeResult(row=(10,))

        if "FROM shop" in q:
            return FakeResult(rows=[("sword", 10, 5)])

        if "playerItems" in q:
            return FakeResult(row=(3,))

        return FakeResult()

    #  REQUIRED FOR "with engine.begin()"
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class FakeEngine:
    def begin(self):
        return FakeConn()


@pytest.fixture
def fake_engine():
    return FakeEngine()


# =========================================================
# OTHER FAKES (YOUR EXISTING)
# =========================================================

class FakeRNG:
    def randint(self, a, b):
        return 10

    def choice(self, items):
        return items[0]


class FakeQuestManager:
    def __init__(self):
        self.updated_enemy = None

    def update(self, enemy):
        self.updated_enemy = enemy


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


# =========================================================
# FIXTURE EXPORTS
# =========================================================

@pytest.fixture
def fake_rng():
    return FakeRNG()


@pytest.fixture
def fake_quest_manager():
    return FakeQuestManager()


@pytest.fixture
def fake_shop_repo():
    return FakeShopRepo()