from app.core.questManager import QuestManager


class FakePlayer:
    pass


class FakeQuest:
    def __init__(self, completed=False):
        self.completed = completed
        self.unlocked = False
        self.calls = []

    def update(self, enemyName, player):
        self.calls.append((enemyName, player))
        return self.completed


def test_update_lowercases_enemy_name():
    player = FakePlayer()
    quest = FakeQuest()

    manager = QuestManager([quest], player)

    manager.update("GOBLIN")

    assert quest.calls[0][0] == "goblin"


def test_update_passes_player_to_quest():
    player = FakePlayer()
    quest = FakeQuest()

    manager = QuestManager([quest], player)

    manager.update("Goblin")

    assert quest.calls[0][1] is player


def test_completed_quest_unlocks_next_quest():
    player = FakePlayer()

    firstQuest = FakeQuest(completed=True)
    secondQuest = FakeQuest()

    manager = QuestManager(
        [firstQuest, secondQuest],
        player,
    )

    manager.update("Goblin")

    assert secondQuest.unlocked is True


def test_last_quest_does_not_crash_when_completed():
    player = FakePlayer()

    lastQuest = FakeQuest(completed=True)

    manager = QuestManager([lastQuest], player)

    manager.update("Goblin")

    assert lastQuest.unlocked is False


def test_unlock_next_quest_directly():
    player = FakePlayer()

    firstQuest = FakeQuest()
    secondQuest = FakeQuest()

    manager = QuestManager(
        [firstQuest, secondQuest],
        player,
    )

    manager.unlockNextQuest(firstQuest)

    assert secondQuest.unlocked is True