from app.services.combatService import CombatService
from app.models.player import Player


def make_enemy():
    return {
        "name": "Goblin",
        "hp": 10,
        "attack": 5,
        "xp": 10,
        "gold": 5
    }


def test_combat_service_default():
    service = CombatService()

    player = Player(0)
    enemies = [make_enemy()]

    result = service.handleFight(player, enemies)

    assert result is not None
    assert "result" in result
    assert "log" in result