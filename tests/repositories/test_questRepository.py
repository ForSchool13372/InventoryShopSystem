import pytest
from app.repositories.questRepository import QuestRepository


# =========================================================
# FAKE DB LAYER (SQLALCHEMY STYLE)
# =========================================================

class FakeResult:
    def __init__(self, rows=None):
        self._rows = rows or []

    def mappings(self):
        return self

    def all(self):
        return self._rows


class FakeConn:
    def __init__(self):
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((str(query), params))

        q = str(query).lower()

        # -------------------------
        # LOAD QUESTS
        # -------------------------
        if "from quests" in q:
            return FakeResult([
                {
                    "name": "Goblin Slayer",
                    "targetenemy": "Goblin",
                    "target": 5,
                    "rewardxp": 100,
                    "rewardgold": 50,
                    "progress": 3,
                    "completed": False,
                    "unlocked": True,
                    "claimed": False
                }
            ])

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

def test_load_quests(monkeypatch):
    repo = QuestRepository()

    monkeypatch.setattr(
        "app.repositories.questRepository.engine",
        FakeEngine()
    )

    result = repo.loadQuests(1)

    assert len(result) == 1

    quest = result[0]

    assert quest["name"] == "Goblin Slayer"
    assert quest["targetenemy"] == "Goblin"
    assert quest["target"] == 5
    assert quest["rewardxp"] == 100
    assert quest["rewardgold"] == 50
    assert quest["progress"] == 3
    assert quest["completed"] is False
    assert quest["unlocked"] is True
    assert quest["claimed"] is False


def test_save_quests_dict(monkeypatch):
    repo = QuestRepository()

    monkeypatch.setattr(
        "app.repositories.questRepository.engine",
        FakeEngine()
    )

    quests = [
        {
            "name": "Goblin Slayer",
            "progress": 5,
            "completed": True,
            "unlocked": True,
            "claimed": False
        }
    ]

    repo.saveQuests(1, quests)

    assert True


def test_save_quests_object(monkeypatch):
    repo = QuestRepository()

    monkeypatch.setattr(
        "app.repositories.questRepository.engine",
        FakeEngine()
    )

    class Quest:
        def __init__(self):
            self.name = "Goblin Slayer"
            self.progress = 5
            self.completed = True
            self.unlocked = True
            self.claimed = False

    repo.saveQuests(1, [Quest()])

    assert True