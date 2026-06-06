import random
from app.models.enemy import Enemy


# =========================================================
# DAMAGE SYSTEM (injectable RNG)
# =========================================================

def dealPlayerDamage(rng=random):
    return rng.randint(5, 15)


def dealEnemyDamage(enemy, rng=random):
    minDamage = getattr(enemy, "minDamage", getattr(enemy, "attack", 1))
    maxDamage = getattr(enemy, "maxDamage", getattr(enemy, "attack", 3))
    return rng.randint(minDamage, maxDamage)


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
# MAIN FIGHT FUNCTION (TEST SAFE)
# =========================================================

def fight(player, enemies, rng=random):
    enemyTemplate = rng.choice(enemies)

    # fallback-safe extraction (supports BOTH test + real model)
    name = getattr(enemyTemplate, "name", "enemy")
    hp = getattr(enemyTemplate, "maxHp", getattr(enemyTemplate, "hp", 10))
    xp = getattr(enemyTemplate, "xp", 10)

    minDamage = getattr(enemyTemplate, "minDamage", getattr(enemyTemplate, "attack", 1))
    maxDamage = getattr(enemyTemplate, "maxDamage", getattr(enemyTemplate, "attack", 3))

    enemy = Enemy(name, hp, xp, minDamage, maxDamage)

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