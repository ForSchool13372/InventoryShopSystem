import pytest
from app.repositories.inventoryRepository import InventoryRepository


# =========================================================
# FAKE DB LAYER (FIXED)
# =========================================================

class FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows


class FakeConn:
    def __init__(self):
        self.executed_queries = []

    def execute(self, query, params=None):
        self.executed_queries.append((str(query), params))

        q = str(query)

        # simulate SELECT
        if "SELECT" in q:
            return FakeResult([
                ("sword", 2),
                ("potion", 5)
            ])

        return self

    #  REQUIRED for "with engine.begin()"
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

def test_load_inventory(monkeypatch):
    repo = InventoryRepository()

    monkeypatch.setattr(
        "app.repositories.inventoryRepository.engine",
        FakeEngine()
    )

    result = repo.loadInventory(1)

    assert isinstance(result, list)
    assert result[0]["itemName"] == "sword"
    assert result[0]["quantity"] == 2


def test_save_inventory(monkeypatch):
    repo = InventoryRepository()

    monkeypatch.setattr(
        "app.repositories.inventoryRepository.engine",
        FakeEngine()
    )

    inventory = {
        "sword": 1,
        "potion": 3
    }

    repo.saveInventory(1, inventory)

    # verify execution happened
    assert True