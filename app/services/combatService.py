import random
import secrets


class CombatService:
    def handleFight(self, player, enemies):

        # 🔒 EARLY EXIT: no fight if dead
        if player.core["hp"] <= 0:
            return {
                "result": "lose",
                "enemy": None,
                "xp": 0,
                "gold": 0,
                "log": ["💀 You are already defeated."],
                "startingPlayerHp": player.core["hp"],
                "finalPlayerHp": player.core["hp"]
            }

        enemy = secrets.choice(enemies)

        startingHp = enemy.hp
        startingPlayerHp = player.core["hp"]

        log = []
        turn = 1

        log.append(f"⚔️ A wild {enemy.name} appears!")

        while True:

            # PLAYER TURN
            damage = player.combat["attack"]

            if random.random() < player.combat["critchance"]:
                damage *= player.combat["critmultiplier"]

                log.append(
                    f"Turn {turn}: 💥 CRITICAL HIT! You deal {int(damage)} damage."
                )

            else:
                log.append(
                    f"Turn {turn}: ⚔️ You deal {damage} damage."
                )

            enemy.takeDamage(damage)

            if enemy.isDead():
                break


            # ENEMY TURN
            actualDamage = player.takeDamage(enemy.attack)

            log.append(
                f"Turn {turn}: 🩸 {enemy.name} hits you for {actualDamage} damage."
            )

            if player.isDead():
                break

            turn += 1


        finalHp = enemy.hp
        finalPlayerHp = player.core["hp"]


        # RESULT
        if player.core["hp"] > 0:
            result = "win"

            log.append(
                f"🏆 You defeated {enemy.name}!"
            )

            log.append(
                f"⭐ +{enemy.xp} XP | 💰 +{enemy.gold} gold"
            )

        else:
            result = "lose"

            log.append(
                f"💀 You were defeated by {enemy.name}..."
            )


        return {
            "result": result,
            "enemy": enemy,
            "xp": enemy.xp,
            "gold": enemy.gold,
            "log": log,

            # Enemy HP tracking
            "startingHp": startingHp,
            "finalHp": finalHp,

            # Player HP tracking
            "startingPlayerHp": startingPlayerHp,
            "finalPlayerHp": finalPlayerHp
        }