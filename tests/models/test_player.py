import pytest
from app.models.player import Player


def test_player_initialization_defaults():
    player = Player(gold=50)

    assert player.gold == 50
    assert player.hp == 100
    assert player.level == 1
    assert player.xp == 0


def test_take_damage_reduces_hp_not_below_zero():
    player = Player(gold=0, hp=20)

    player.takeDamage(5)
    assert player.hp == 15

    player.takeDamage(100)
    assert player.hp == 0


def test_revive_restores_hp():
    player = Player(gold=0, hp=10)

    player.revive()

    assert player.hp == 100


def test_gain_xp_no_level_up():
    player = Player(gold=0)

    result = player.gainXP(50)

    assert player.xp == 50
    assert player.level == 1
    assert result["leveledUp"] is False


def test_gain_xp_with_level_up():
    player = Player(gold=0, xp=80)

    result = player.gainXP(50)

    assert player.level == 2
    assert player.xp == 30
    assert result["leveledUp"] is True


def test_to_dict_returns_correct_structure():
    player = Player(gold=10, hp=80, level=3, xp=40)

    result = player.toDict()

    assert result == {
        "gold": 10,
        "level": 3,
        "xp": 40,
        "hp": 80,
    }


def test_get_stats_returns_same_structure():
    player = Player(gold=10, hp=80, level=3, xp=40)

    assert player.getStats() == {
        "gold": 10,
        "level": 3,
        "xp": 40,
        "hp": 80,
    }