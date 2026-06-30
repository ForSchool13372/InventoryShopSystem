import pytest
from app.models.enemy import Enemy


def test_enemy_initialization_sets_all_fields():
    enemy = Enemy(
        name="Goblin",
        hp=100,
        xp=50,
        gold=10,
        minDamage=5,
        maxDamage=10,
    )

    assert enemy.name == "Goblin"
    assert enemy.maxHp == 100
    assert enemy.hp == 100
    assert enemy.xp == 50
    assert enemy.gold == 10
    assert enemy.minDamage == 5
    assert enemy.maxDamage == 10


def test_take_damage_reduces_hp_but_not_below_zero():
    enemy = Enemy("Goblin", 20, 10, 5, 1, 3)

    enemy.takeDamage(5)
    assert enemy.hp == 15

    enemy.takeDamage(50)
    assert enemy.hp == 0


def test_reset_restores_full_hp():
    enemy = Enemy("Goblin", 30, 10, 5, 1, 3)

    enemy.takeDamage(10)
    assert enemy.hp == 20

    enemy.reset()
    assert enemy.hp == 30


def test_to_dict_returns_correct_structure():
    enemy = Enemy("Goblin", 100, 50, 10, 5, 10)

    result = enemy.toDict()

    assert result == {
        "name": "Goblin",
        "maxHp": 100,
        "hp": 100,
        "xp": 50,
        "gold": 10,
        "minDamage": 5,
        "maxDamage": 10,
        "attack": 7,
    }