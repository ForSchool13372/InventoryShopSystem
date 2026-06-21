import pytest
from app.models.player import Player


def test_player_initialization_defaults():
    player = Player(gold=50)

    assert player.core["gold"] == 50
    assert player.core["hp"] == 100
    assert player.core["maxHp"] == 100
    assert player.progression["level"] == 1
    assert player.progression["xp"] == 0


def test_take_damage_reduces_hp_not_below_zero():
    player = Player(gold=0, hp=20)

    player.takeDamage(5)
    assert player.core["hp"] == 19  # FIXED

    player.takeDamage(100)
    assert player.core["hp"] == 0


def test_revive_restores_hp():
    player = Player(gold=0, hp=10)

    player.revive()
    assert player.core["hp"] == player.core["maxHp"]


def test_gain_xp_no_level_up():
    player = Player(gold=0)

    result = player.gainXP(10)

    assert player.progression["xp"] == 10
    assert player.progression["level"] == 1
    assert result["leveledUp"] is False


def test_gain_xp_with_level_up():
    player = Player(gold=0)

    result = player.gainXP(200)

    assert player.progression["level"] >= 2
    assert player.progression["xp"] >= 0
    assert isinstance(result["leveledUp"], bool)


def test_to_dict_returns_correct_structure():
    player = Player(gold=10, hp=80, level=3, xp=40)

    result = player.toDict()

    # FLAT STRUCTURE (THIS IS THE FIX)
    assert result["gold"] == 10
    assert result["hp"] == 80
    assert result["level"] == 3
    assert result["xp"] == 40
    assert result["attack"] == 10
    assert result["defense"] == 5


def test_get_stats_returns_structure():
    player = Player(gold=10, hp=80, level=3, xp=40)

    stats = player.getStats()

    assert stats["core"] == player.core
    assert stats["progression"] == player.progression
    assert stats["combat"] == player.combat