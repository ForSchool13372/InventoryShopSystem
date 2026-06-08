import pytest
from app.repositories.shopRepository import ShopRepository


# =========================================================
# FAKE DB LAYER (SQLALCHEMY STYLE)
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

        q = str(query).lower()

        # -------------------------
        # getShopStock
        # -------------------------
        if "from shop" in q and "where" not in q:
            return FakeResult(rows=[
                ("sword", 10, 5),
                ("potion", 20, 2)
            ])

        # -------------------------
        # getStock
        # -------------------------
        if "select stock" in q and "where" in q:
            return FakeResult(row=(10,))

        # -------------------------
        # getPlayerItemQuantity
        # -------------------------
        if "from playeritems" in q:
            return FakeResult(row=(3,))

        # -------------------------
        # removePlayerItem DELETE
        # -------------------------
        if "delete from playeritems" in q:
            return FakeResult()

        return FakeResult()

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
    assert result[0]["itemName"] == "sword"
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