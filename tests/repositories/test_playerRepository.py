import pytest
from app.repositories.playerRepository import PlayerRepository


# =========================================================
# FAKE DB LAYER (SQLALCHEMY STYLE)
# =========================================================

class FakeResult:
    def __init__(self, row=None):
        self._row = row

    def mappings(self):
        return self

    def fetchone(self):
        return self._row


class FakeConn:
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((str(query), params))

        q = str(query).lower()

        # -------------------------
        # LOAD PLAYER SUCCESS
        # -------------------------
        if "from player" in q and "where id" in q:
            return FakeResult({
                "gold": 100,
                "hp": 50,
                "level": 1,
                "xp": 10
            })

        return FakeResult(None)

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

def test_load_player(monkeypatch):
    repo = PlayerRepository()

    monkeypatch.setattr(
        "app.repositories.playerRepository.engine",
        FakeEngine()
    )

    result = repo.load(1)

    assert isinstance(result, dict)
    assert result["gold"] == 100
    assert result["hp"] == 50
    assert result["level"] == 1
    assert result["xp"] == 10


def test_load_player_not_found(monkeypatch):
    repo = PlayerRepository()

    class EmptyConn(FakeConn):
        def execute(self, query, params=None):
            self.executed.append((str(query), params))
            return FakeResult(None)

    class EmptyEngine:
        def begin(self):
            return EmptyConn()

    monkeypatch.setattr(
        "app.repositories.playerRepository.engine",
        EmptyEngine()
    )

    result = repo.load(999)

    assert result is None


def test_save_player_dict(monkeypatch):
    repo = PlayerRepository()

    monkeypatch.setattr(
        "app.repositories.playerRepository.engine",
        FakeEngine()
    )

    class PlayerObj:
        def __init__(self, d):
            self.gold = d["gold"]
            self.hp = d["hp"]
            self.level = d["level"]
            self.xp = d["xp"]

        def toDict(self):
            return {
                "gold": self.gold,
                "hp": self.hp,
                "level": self.level,
                "xp": self.xp
            }

    player = PlayerObj({
        "gold": 200,
        "hp": 80,
        "level": 2,
        "xp": 20
    })

    repo.save(1, player)

    assert True


def test_save_player_object(monkeypatch):
    repo = PlayerRepository()

    monkeypatch.setattr(
        "app.repositories.playerRepository.engine",
        FakeEngine()
    )

    class PlayerObj:
        def __init__(self):
            self.gold = 200
            self.hp = 80
            self.level = 2
            self.xp = 20

        def toDict(self):
            return {
                "gold": self.gold,
                "hp": self.hp,
                "level": self.level,
                "xp": self.xp
            }

    repo.save(1, PlayerObj())

    assert True