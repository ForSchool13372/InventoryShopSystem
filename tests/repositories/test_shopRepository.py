import pytest
from app.repositories.shopRepository import ShopRepository


# =========================================================
# FAKE SQLALCHEMY RESULT (supports .mappings())
# =========================================================

class FakeMappings:
    def __init__(self, data):
        self._data = data

    def all(self):
        return self._data

    def fetchone(self):
        return self._data[0] if self._data else None


class FakeResult:
    def __init__(self, data=None):
        self._data = data or []

    def mappings(self):
        return FakeMappings(self._data)


# =========================================================
# FAKE CONNECTION
# =========================================================

class FakeConn:
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((str(query), params))
        q = str(query).lower()

        # -------------------------
        # getShopStock
        # -------------------------
        if "from shop" in q and "select" in q:
            return FakeResult([
                {"itemname": "sword", "stock": 10, "price": 5}
            ])

        # -------------------------
        # getStock
        # -------------------------
        if "from shop" in q and "where" in q:
            return FakeResult([
                {"stock": 10}
            ])

        # -------------------------
        # getPlayerItemQuantity
        # -------------------------
        if "from playeritems" in q:
            return FakeResult([
                {"quantity": 3}
            ])

        # default (for update/insert/delete)
        return FakeResult([])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class FakeEngine:
    def begin(self):
        return FakeConn()


# =========================================================
# TESTS
# =========================================================

def test_get_shop_stock():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    result = repo.getShopStock(conn)

    assert isinstance(result, list)
    assert result[0]["itemname"] == "sword"
    assert result[0]["stock"] == 10
    assert result[0]["price"] == 5


def test_get_stock():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    result = repo.getStock(conn, "sword")

    assert "stock" in result
    assert result["stock"] == 10


def test_get_player_item_quantity():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    result = repo.getPlayerItemQuantity(conn, 1, "sword")

    assert "quantity" in result
    assert result["quantity"] == 3


def test_decrease_stock():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    repo.decreaseStock(conn, "sword", 2)

    assert len(conn.executed) == 1


def test_increase_stock():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    repo.increaseStock(conn, "sword", 2)

    assert len(conn.executed) == 1


def test_add_or_update_player_item():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    repo.addOrUpdatePlayerItem(conn, 1, "sword", 2)

    assert len(conn.executed) == 1


def test_remove_player_item():
    repo = ShopRepository()
    conn = FakeEngine().begin()

    repo.removePlayerItem(conn, 1, "sword", 2)

    assert len(conn.executed) == 2