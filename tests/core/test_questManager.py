from app.core.game.questManager import QuestManager


class FakePlayer:
    pass


class FakeQuest:
    def __init__(self, completed=False, name="Quest"):
        self.name = name
        self.completed = completed
        self.unlocked = False
        self.calls = []
        self.rewardXP = 0
        self.rewardGold = 0

    def update(self, enemyName):
        self.calls.append(enemyName)
        return self.completed


def test_update_lowercases_enemy_name():
    player = FakePlayer()
    quest = FakeQuest()

    manager = QuestManager([quest], player, None)

    manager.update("GOBLIN")

    assert quest.calls[0] == "goblin"


def test_update_passes_player_to_quest():
    player = FakePlayer()
    quest = FakeQuest()

    manager = QuestManager([quest], player, None)

    manager.update("Goblin")

    assert quest.calls[0] == "goblin"


def test_completed_quest_unlocks_next_quest():
    player = FakePlayer()

    firstQuest = FakeQuest(completed=True, name="Quest 1")
    secondQuest = FakeQuest(name="Quest 2")

    manager = QuestManager(
        [firstQuest, secondQuest],
        player,
        None,
    )

    manager.update("Goblin")

    assert secondQuest.unlocked is True


def test_last_quest_does_not_crash_when_completed():
    player = FakePlayer()

    lastQuest = FakeQuest(completed=True, name="Quest 1")

    manager = QuestManager([lastQuest], player, None)

    manager.update("Goblin")

    assert lastQuest.unlocked is False


def test_unlock_next_quest_directly():
    player = FakePlayer()

    firstQuest = FakeQuest(name="Quest 1")
    secondQuest = FakeQuest(name="Quest 2")

    manager = QuestManager(
        [firstQuest, secondQuest],
        player,
        None,
    )

    manager.unlockNextQuest(firstQuest)

    assert secondQuest.unlocked is True