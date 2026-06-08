from app.services.combat import fight
from app.services.combatService import CombatService


# =========================================================
# FIXTURES (INLINE FAKES)
# =========================================================

class Player:
    def __init__(self):
        self.hp = 100
        self.level = 1

    def takeDamage(self, dmg):
        self.hp -= dmg


class Enemy:
    def __init__(self):
        self.name = "goblin"
        self.hp = 10
        self.attack = 1

    def takeDamage(self, dmg):
        self.hp -= dmg


# =========================================================
# TESTS
# =========================================================

def test_fight_basic():
    player = Player()
    enemy = Enemy()

    result = fight(player, [enemy])

    assert isinstance(result, dict)
    assert "result" in result
    assert "xp" in result
    assert "enemy" in result
    assert "logs" in result


def test_combat_service():
    service = CombatService()

    player = Player()
    enemy = Enemy()

    result = service.handleFight(player, [enemy])

    assert isinstance(result, dict)
    assert "result" in result