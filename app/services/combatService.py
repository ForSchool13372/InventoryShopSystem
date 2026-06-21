import random


class CombatService:
    def __init__(self):
        pass

    # =========================================================
    # HELPERS (makes hybrid system safe)
    # =========================================================
    def _get(self, obj, key):
        if isinstance(obj, dict):
            return obj[key]
        return getattr(obj, key)

    # =========================================================
    # PUBLIC API
    # =========================================================
    def handleFight(self, player, enemies):

        enemy = random.choice(enemies)

        # =========================
        # SAFE PLAYER STATS
        # =========================
        playerStats = getattr(player, "combat", {
            "attack": 10,
            "critChance": 0,
            "critMultiplier": 1.5,
            "defense": 0
        })

        enemyHp = self._get(enemy, "hp")
        enemyAttack = self._get(enemy, "attack")
        enemyName = self._get(enemy, "name")

        log = []
        turn = 1

        while self._get(player, "core")["hp"] > 0 and enemyHp > 0:

            # =========================
            # PLAYER TURN
            # =========================
            damage = playerStats["attack"]

            if random.random() < playerStats["critChance"]:
                damage *= playerStats["critMultiplier"]
                log.append(
                    f"Turn {turn}: 💥 CRITICAL HIT! You deal {damage} damage to {enemyName}."
                )
            else:
                log.append(
                    f"Turn {turn}: ⚔️ You deal {damage} damage to {enemyName}."
                )

            enemyHp -= damage

            if enemyHp <= 0:
                break

            # =========================
            # ENEMY TURN
            # =========================
            player.takeDamage(enemyAttack)

            log.append(
                f"Turn {turn}: 🩸 {enemyName} deals {enemyAttack} damage to you."
            )

            turn += 1

        # =========================
        # RESULT
        # =========================
        if self._get(player, "core")["hp"] > 0:
            result = "win"
            log.append(f"🏆 You defeated {enemyName}!")
            log.append(f"⭐ You gained {self._get(enemy, 'xp')} XP!")
            log.append(f"💰 You gained {self._get(enemy, 'gold')} gold!")

        else:
            result = "lose"
            log.append(f"💀 You were defeated by {enemyName}!")

        return {
            "result": result,
            "enemy": enemy,
            "xp": self._get(enemy, "xp"),
            "gold": self._get(enemy, "gold"),
            "log": log
        }