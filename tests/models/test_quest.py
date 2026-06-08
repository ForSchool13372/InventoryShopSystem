import pytest
from app.models.quest import Quest


class FakePlayer:
    def __init__(self):
        self.xp = 0

    def gainXP(self, amount):
        self.xp += amount


def test_quest_initial_state():
    quest = Quest("Slay Goblins", "goblin", 3, 50)

    assert quest.name == "Slay Goblins"
    assert quest.targetEnemy == "goblin"
    assert quest.target == 3
    assert quest.progress == 0
    assert quest.rewardXP == 50
    assert quest.completed is False
    assert quest.unlocked is False


def test_update_does_nothing_if_locked():
    quest = Quest("Slay Goblins", "goblin", 2, 50)
    player = FakePlayer()

    result = quest.update("goblin", player)

    assert result is False
    assert quest.progress == 0


def test_update_increments_progress_when_unlocked():
    quest = Quest("Slay Goblins", "goblin", 2, 50)
    quest.unlocked = True
    player = FakePlayer()

    result = quest.update("goblin", player)

    assert quest.progress == 1
    assert result is False


def test_update_ignores_wrong_enemy():
    quest = Quest("Slay Goblins", "goblin", 2, 50)
    quest.unlocked = True
    player = FakePlayer()

    result = quest.update("orc", player)

    assert result is False
    assert quest.progress == 0


def test_quest_completes_and_grants_xp():
    quest = Quest("Slay Goblins", "goblin", 1, 50)
    quest.unlocked = True
    player = FakePlayer()

    result = quest.update("goblin", player)

    assert result is True
    assert quest.completed is True
    assert player.xp == 50


def test_update_after_completion_does_nothing():
    quest = Quest("Slay Goblins", "goblin", 1, 50)
    quest.unlocked = True
    player = FakePlayer()

    quest.update("goblin", player)
    result = quest.update("goblin", player)

    assert result is False
    assert quest.progress == 1