import random
from enemy import Enemy

def dealPlayerDamage():
    return random.randint(5, 15)

def dealEnemyDamage(enemy):
    return random.randint(enemy.minDamage, enemy.maxDamage)

def combatRound(player, enemy):
    logs = []

    # Player attacks
    damage = dealPlayerDamage()
    enemy.takeDamage(damage)
    logs.append(f"You deal {damage} damage. Enemy HP: {enemy.hp}")

    if enemy.hp <= 0:
        return logs

    # Enemy attacks
    enemyDamage = dealEnemyDamage(enemy)
    player.takeDamage(enemyDamage)
    logs.append(f"Enemy hits you for {enemyDamage}. Your HP: {player.hp}")

    return logs

def fight(player, enemies):
    enemyTemplate = random.choice(enemies)

    enemy = Enemy(
        enemyTemplate.name,
        enemyTemplate.maxHp,
        enemyTemplate.xp,
        enemyTemplate.minDamage,
        enemyTemplate.maxDamage
    )

    print(f"You fight a {enemy.name}!")

    while enemy.hp > 0 and player.hp > 0:
        logs = combatRound(player, enemy)
        for log in logs:
            print(log)

    if player.hp <= 0:
        return {
            "result": "lose",
            "enemy": enemy.name,
            "xp": 0
        }

    return {
        "result": "win",
        "enemy": enemy.name,
        "xp": enemy.xp
    }