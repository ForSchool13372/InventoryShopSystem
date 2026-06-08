from types import SimpleNamespace
from app.services.shopService import ShopService


# =========================================================
# FAKE OBJECTS
# =========================================================

class FakeItem:
    def __init__(self, name="sword", price=10):
        self.name = name
        self.price = price


class FakePlayer:
    def __init__(self):
        self.gold = 100


def make_ctx(item, quantity=1, playerId=1):
    return SimpleNamespace(
        item=item,
        quantity=quantity,
        playerId=playerId,
        player=FakePlayer()
    )


# =========================================================
# FAKE REPOS
# =========================================================

class FakeShopRepoGet:
    def getShopStock(self, conn):
        return {"data": ["sword", "potion"]}


class FakeShopRepoBuy:
    def getStock(self, conn, itemName):
        return {"stock": 10}

    def decreaseStock(self, conn, itemName, quantity):
        pass

    def addOrUpdatePlayerItem(self, conn, playerId, itemName, quantity):
        pass


class FakeShopRepoSell:
    def getPlayerItemQuantity(self, conn, playerId, itemName):
        return {"quantity": 10}

    def removePlayerItem(self, conn, playerId, itemName, quantity):
        pass

    def increaseStock(self, conn, itemName, quantity):
        pass


# =========================================================
# TESTS
# =========================================================

def test_shop_service_get_shop():
    service = ShopService(FakeShopRepoGet())

    result = service.getShop()

    assert isinstance(result, dict)
    assert "data" in result


def test_shop_service_buy_success():
    service = ShopService(FakeShopRepoBuy())

    ctx = make_ctx(FakeItem(), quantity=1)

    result = service.buy(ctx)

    assert result["success"] is True


def test_shop_service_sell_success():
    service = ShopService(FakeShopRepoSell())

    ctx = make_ctx(FakeItem(), quantity=1)

    result = service.sell(ctx)

    assert result["success"] is True