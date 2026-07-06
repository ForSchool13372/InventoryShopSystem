from app.services.combatService import CombatService
from app.models.player import Player
from app.models.enemy import Enemy


def make_enemy():
    return Enemy(
        name="Boss Goblin",
        hp=50,
        xp=10,
        gold=5,
        minDamage=15,
        maxDamage=15
    )


def test_combat_logs_until_player_death():
    service = CombatService()

    # Player starts weak enough to die after a few hits
    player = Player(0)
    player.core["hp"] = 40
    player.combat["attack"] = 10
    player.combat["critchance"] = 0 
    player.combat["critmultiplier"] = 1

    enemies = [make_enemy()]

    result = service.handleFight(player, enemies)
    log = result["log"]

    # Core behavior checks
    assert result["result"] == "lose"
    assert log[-1] == "💀 You were defeated by Boss Goblin..."

    # Ensure fight lasted multiple turns
    turnCount = sum(1 for line in log if "Turn" in line)
    assert turnCount >= 2