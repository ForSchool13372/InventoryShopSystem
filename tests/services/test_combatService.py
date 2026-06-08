from app.services.combatService import CombatService


# =========================================================
# SHARED FAKE OBJECTS
# =========================================================

class Player:
    def __init__(self):
        self.hp = 100

    def takeDamage(self, amount):
        self.hp -= amount


class Enemy:
    def __init__(self):
        self.hp = 10

    def takeDamage(self, amount):
        self.hp -= amount


# =========================================================
# TESTS
# =========================================================

def test_combat_service_default_engine_runs():
    service = CombatService()

    player = Player()
    enemies = [Enemy()]

    result = service.handleFight(player, enemies)

    assert result is not None


def test_combat_service_injected_engine():
    def fakeEngine(player, enemies):
        return {
            "result": "win",
            "xp": 10
        }

    service = CombatService(combatEngine=fakeEngine)

    player = Player()
    enemies = [Enemy()]

    result = service.handleFight(player, enemies)

    assert result["result"] == "win"
    assert result["xp"] == 10
