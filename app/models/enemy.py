import random


class Enemy:
    def __init__(
        self,
        name: str,
        hp: int,
        xp: int,
        gold: int,
        minDamage: int,
        maxDamage: int
    ):
        self.name = name

        # =========================
        # COMBAT STATS
        # =========================
        self.maxHp = hp
        self.hp = hp

        self.minDamage = minDamage
        self.maxDamage = maxDamage

        # compatibility stat
        self.attack = (minDamage + maxDamage) // 2

        # =========================
        # REWARDS
        # =========================
        self.xp = xp
        self.gold = gold

    # =========================================================
    # COMBAT
    # =========================================================
    def takeDamage(self, damage: int):
        self.hp = max(0, self.hp - damage)

    def dealDamage(self):
        return random.randint(self.minDamage, self.maxDamage)

    def reset(self):
        self.hp = self.maxHp

    def isDead(self):
        return self.hp <= 0

    # =========================================================
    # SERIALIZATION
    # =========================================================
    def toDict(self):
        return {
            "name": self.name,
            "maxHp": self.maxHp,
            "hp": self.hp,
            "xp": self.xp,
            "gold": self.gold,
            "minDamage": self.minDamage,
            "maxDamage": self.maxDamage,
            "attack": self.attack
        }