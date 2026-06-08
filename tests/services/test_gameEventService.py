from app.services.gameEventService import GameEventService


# =========================================================
# FAKE OBJECTS
# =========================================================

class FakePlayer:
    def __init__(self):
        self.hp = 100
        self.id = 1
        self.xp = 0

    def gainXP(self, amount):
        self.xp += amount


class FakeQuestManager:
    def __init__(self):
        self.updated_enemy = None

    def update(self, enemy):
        self.updated_enemy = enemy


# =========================================================
# TESTS
# =========================================================

def test_game_event_service_creates_instance():
    service = GameEventService(FakePlayer(), FakeQuestManager())

    assert service is not None
    assert service.eventHistory == []


def test_game_event_handle_fight_win():
    player = FakePlayer()
    qm = FakeQuestManager()
    service = GameEventService(player, qm)

    event = {
        "type": "fightWin",
        "xp": 10,
        "enemy": {"name": "goblin"}
    }

    service.handleEvent(event)

    assert player.xp == 10
    assert qm.updated_enemy is not None
    assert len(service.eventHistory) == 1


def test_game_event_handle_fight_lose():
    player = FakePlayer()
    qm = FakeQuestManager()
    service = GameEventService(player, qm)

    event = {"type": "fightLose"}

    service.handleEvent(event)

    assert player.hp == 0
    assert len(service.eventHistory) == 1


def test_game_event_history_limit():
    service = GameEventService(FakePlayer(), FakeQuestManager())

    for i in range(5):
        service.handleEvent({
            "type": "fightWin",
            "xp": 1,
            "enemy": {"id": i}
        })

    events = service.getEvents(limit=2)

    assert len(events) == 2