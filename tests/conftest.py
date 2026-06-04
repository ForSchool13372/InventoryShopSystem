import pytest

from app.models.item import Item
from app.models.player import Player
from app.models.enemy import Enemy


# =========================================================
# FIXTURES (FACTORIES)
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
# TEST DOUBLES (FAKES)
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


# =========================================================
# FAKE SHOP REPO (UPDATED FOR NEW SERVICE DESIGN)
# =========================================================

class FakeShopRepo:
    def __init__(self):
        self.stock = {"sword": 10, "potion": 10}
        self.playerItems = {}

    # =========================================================
    # STOCK (MATCH REAL INTERFACE)
    # =========================================================

    def getStock(self, conn, itemName):
        if itemName not in self.stock:
            return None
        return (self.stock[itemName],)

    def decreaseStock(self, conn, itemName, quantity):
        self.stock[itemName] -= quantity

    def increaseStock(self, conn, itemName, quantity):
        self.stock[itemName] = self.stock.get(itemName, 0) + quantity

    # =========================================================
    # PLAYER ITEMS (MATCH REAL INTERFACE)
    # =========================================================

    def addOrUpdatePlayerItem(self, conn, playerId, itemName, quantity):
        self.playerItems[itemName] = self.playerItems.get(itemName, 0) + quantity

    def removePlayerItem(self, conn, playerId, itemName, quantity):
        if itemName in self.playerItems:
            self.playerItems[itemName] -= quantity
            if self.playerItems[itemName] <= 0:
                del self.playerItems[itemName]

    def getPlayerItemQuantity(self, conn, playerId, itemName):
        return self.playerItems.get(itemName, 0)


# =========================================================
# FIXTURES (EXPOSE FAKES TO TESTS)
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