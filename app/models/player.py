class Player:
    def __init__(self, gold: int, hp: int = 100, level: int = 1, xp: int = 0):
        self.gold = gold
        self.hp = hp
        self.level = level
        self.xp = xp


    # =========================================================
    # COMBAT
    # =========================================================

    def takeDamage(self, damage: int):
        self.hp = max(0, self.hp - damage)


    def revive(self):
        self.hp = 100


    # =========================================================
    # PROGRESSION SYSTEM
    # =========================================================

    def gainXP(self, amount: int):
        self.xp += amount

        leveledUp = False

        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            leveledUp = True

        return {
            "leveledUp": leveledUp,
            "level": self.level,
            "xp": self.xp
        }


    # =========================================================
    # SERIALIZATION (SAVE/LOAD)
    # =========================================================

    def fromDict(self, data: dict):
        self.gold = data.get("gold", 0)
        self.level = data.get("level", 1)
        self.xp = data.get("xp", 0)
        self.hp = data.get("hp", 100)


    def toDict(self):
        return {
            "gold": self.gold,
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
        }


    # =========================================================
    # DEBUG / DISPLAY (NO SIDE EFFECTS)
    # =========================================================

    def getStats(self):
        return {
            "gold": self.gold,
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
        }