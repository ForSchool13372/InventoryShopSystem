import random
from app.models.enemy import Enemy


# =========================================================
# DAMAGE SYSTEM (injectable RNG)
# =========================================================

def dealPlayerDamage(rng=random):
    return rng.randint(5, 15)


def dealEnemyDamage(enemy, rng=random):
    return rng.randint(enemy.minDamage, enemy.maxDamage)


# =========================================================
# CORE COMBAT LOGIC
# =========================================================

def combatRound(player, enemy, rng=random):
    logs = []

    damage = dealPlayerDamage(rng)
    enemy.takeDamage(damage)

    logs.append({
        "type": "player_damage",
        "value": damage,
        "enemyHp": enemy.hp
    })

    if enemy.hp <= 0:
        return logs

    enemyDamage = dealEnemyDamage(enemy, rng)
    player.takeDamage(enemyDamage)

    logs.append({
        "type": "enemy_damage",
        "value": enemyDamage,
        "playerHp": player.hp
    })

    return logs


# =========================================================
# MAIN FIGHT FUNCTION
# =========================================================

def fight(player, enemies, rng=random):
    enemyTemplate = rng.choice(enemies)

    enemy = Enemy(
        enemyTemplate.name,
        enemyTemplate.maxHp,
        enemyTemplate.xp,
        enemyTemplate.minDamage,
        enemyTemplate.maxDamage
    )

    logs = []

    while enemy.hp > 0 and player.hp > 0:
        logs.extend(combatRound(player, enemy, rng))

    if player.hp <= 0:
        return {
            "result": "lose",
            "enemy": enemy.name,
            "xp": 0,
            "logs": logs
        }

    return {
        "result": "win",
        "enemy": enemy.name,
        "xp": enemy.xp,
        "logs": logs
    }