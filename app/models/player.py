class Player:
    def __init__(self, gold: int, hp: int = 100, maxHp: int = 100, level: int = 1, xp: int = 0):

        # =========================
        # CORE STATS
        # =========================
        self.core = {
            "gold": gold,
            "hp": hp,
            "maxHp": maxHp
        }

        # =========================
        # PROGRESSION
        # =========================
        self.progression = {
            "level": level,
            "xp": xp
        }

        # =========================
        # COMBAT STATS
        # =========================
        self.combat = {
            "attack": 10,
            "defense": 5,
            "critChance": 0.05,
            "critMultiplier": 1.5
        }

    # =========================================================
    # SAFETY
    # =========================================================
    def clampHp(self):
        self.core["hp"] = max(0, min(self.core["hp"], self.core["maxHp"]))

    # =========================================================
    # COMBAT
    # =========================================================
    def takeDamage(self, damage: int):
        reduced = max(1, damage - self.combat["defense"])
        self.core["hp"] -= reduced
        self.clampHp()

    def revive(self):
        self.core["hp"] = self.core["maxHp"]

    def isDead(self):
        return self.core["hp"] <= 0

    # =========================================================
    # PROGRESSION
    # =========================================================
    def getRequiredXp(self):
        # scaling XP curve (smooth RPG progression)
        return int(100 * (1.15 ** (self.progression["level"] - 1)))


    def gainXP(self, amount: int):
        self.progression["xp"] += amount
        leveledUp = False

        while self.progression["xp"] >= self.getRequiredXp():
            requiredXp = self.getRequiredXp()

            self.progression["xp"] -= requiredXp
            self.progression["level"] += 1
            leveledUp = True

            # scaling rewards
            self.core["maxHp"] += 10
            self.core["hp"] = self.core["maxHp"]

            self.combat["attack"] += 2
            self.combat["defense"] += 1

        return {
            "leveledUp": leveledUp,
            "level": self.progression["level"],
            "xp": self.progression["xp"]
    }

    # =========================================================
    # SERIALIZATION
    # =========================================================
    def fromDict(self, data: dict):
        self.core = {
            "gold": data.get("gold", 0),
            "hp": data.get("hp", 100),
            "maxHp": data.get("maxHp", 100)
        }

        self.progression = {
            "level": data.get("level", 1),
            "xp": data.get("xp", 0)
        }

        self.combat = {
            "attack": data.get("attack", 10),
            "defense": data.get("defense", 5),
            "critChance": data.get("critChance", 0.05),
            "critMultiplier": data.get("critMultiplier", 1.5)
        }

        # IMPORTANT: enforce consistency after loading
        self.clampHp()

    def toDict(self):
        return {
            **self.core,
            **self.progression,
            **self.combat
        }

    # =========================================================
    # DEBUG
    # =========================================================
    def getStats(self):
        return {
            "core": self.core,
            "progression": self.progression,
            "combat": self.combat
        }