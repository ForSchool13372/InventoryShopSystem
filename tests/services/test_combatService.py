from app.services.combatService import CombatService
from app.models.player import Player
from app.models.enemy import Enemy


def make_enemy():
    return Enemy(
        name="Goblin",
        hp=10,
        xp=10,
        gold=5,
        minDamage=2,
        maxDamage=5
    )


def test_combat_service_default():
    service = CombatService()

    player = Player(0)
    enemies = [make_enemy()]

    result = service.handleFight(player, enemies)

    assert result is not None
    assert "result" in result
    assert "log" in result