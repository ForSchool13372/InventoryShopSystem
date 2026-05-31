class Enemy:
    def __init__(
        self,
        name: str,
        hp: int,
        xp: int,
        minDamage: int,
        maxDamage: int
    ):
        self.name = name

        # Combat stats
        self.maxHp = hp
        self.hp = hp

        # Rewards
        self.xp = xp

        # Damage range
        self.minDamage = minDamage
        self.maxDamage = maxDamage


    # =========================================================
    # COMBAT
    # =========================================================

    def takeDamage(self, damage: int):
        self.hp = max(0, self.hp - damage)


    def reset(self):
        self.hp = self.maxHp


    # =========================================================
    # SERIALIZATION (optional but good for backend consistency)
    # =========================================================

    def toDict(self):
        return {
            "name": self.name,
            "maxHp": self.maxHp,
            "hp": self.hp,
            "xp": self.xp,
            "minDamage": self.minDamage,
            "maxDamage": self.maxDamage,
        }