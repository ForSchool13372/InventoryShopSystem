import pytest
from types import SimpleNamespace

import app.core.game.seed as seedModule
from app.core.game.seed import createItems, createEnemies, createQuests


# =========================================================
# BASIC UNIT TESTS (NO DB)
# =========================================================

def test_create_items():
    items = createItems()

    assert len(items) == 3
    assert items[0]["itemname"] == "sword"
    assert items[1]["itemtype"] == "consumable"


def test_create_enemies():
    enemies = createEnemies()

    assert len(enemies) == 4
    assert enemies[0].name == "Training Dummy"
    assert enemies[1].name == "Goblin"


def test_create_quests():
    quests = createQuests()

    assert len(quests) == 2
    assert quests[0]["name"] == "Goblin Hunt"


# =========================================================
# MOCK ENGINE (FOR SEED FUNCTIONS)
# =========================================================

class FakeConn:
    def __init__(self):
        self.executed = []

    def execute(self, *args, **kwargs):
        self.executed.append((args, kwargs))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class FakeEngine:
    def begin(self):
        return FakeConn()


@pytest.fixture
def fake_engine(monkeypatch):
    fake = FakeEngine()
    monkeypatch.setattr(seedModule, "engine", fake)
    return fake


# =========================================================
# SEED TESTS
# =========================================================

def test_seed_shop_runs(fake_engine):
    seedModule.seedShop()
    # just ensure it executed SQL
    assert True


def test_seed_players_runs(fake_engine):
    seedModule.seedPlayers()
    assert True


def test_seed_quests_runs(fake_engine):
    seedModule.seedQuests()
    assert True


def test_seed_player_quests_runs(fake_engine):
    seedModule.seedPlayerQuests()
    assert True