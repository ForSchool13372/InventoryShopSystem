class Player:
    def __init__(
        self,
        playerId: int,
        gold: int = 0,
        hp: int = 100,
        maxHp: int = 100,
        level: int = 1,
        xp: int = 0
    ):
        self.playerId = playerId

        # =========================
        # CORE (SAFE DEFAULTS)
        # =========================
        self.core = {
            "gold": gold or 0,
            "hp": hp or 100,
            "maxHp": maxHp or 100
        }

        # =========================
        # PROGRESSION
        # =========================
        self.progression = {
            "level": level or 1,
            "xp": xp or 0
        }

        # =========================
        # COMBAT
        # =========================
        self.combat = {
            "attack": 10,
            "defense": 5,
            "critChance": 0.05,
            "critMultiplier": 1.5
        }

        self.clampHp()

    # =========================
    # HP SYSTEM
    # =========================
    def clampHp(self):
        hp = self.core.get("hp") or 0
        maxHp = self.core.get("maxHp") or 100

        self.core["hp"] = max(0, min(hp, maxHp))
        self.core["maxHp"] = maxHp

    def isDead(self):
        return self.core["hp"] <= 0

    def revive(self):
        self.core["hp"] = self.core["maxHp"]

    # =========================
    # DAMAGE SYSTEM
    # =========================
    def takeDamage(self, damage: int):
        damage = damage or 0
        reduced = max(1, damage - self.combat["defense"])

        self.core["hp"] -= reduced
        self.clampHp()

        return reduced

    # =========================
    # LEVEL SYSTEM
    # =========================
    def getRequiredXp(self):
        return int(100 * (1.15 ** (self.progression["level"] - 1)))

    def gainXP(self, amount: int):
        amount = amount or 0
        self.progression["xp"] += amount

        leveledUp = False

        while self.progression["xp"] >= self.getRequiredXp():
            requiredXp = self.getRequiredXp()

            self.progression["xp"] -= requiredXp
            self.progression["level"] += 1
            leveledUp = True

            self.core["maxHp"] += 10
            self.core["hp"] = min(
                self.core["maxHp"],
                self.core["hp"] + self.core["maxHp"] // 2
            )

            self.combat["attack"] += 2
            self.combat["defense"] += 1

        return {
            "leveledUp": leveledUp,
            "level": self.progression["level"],
            "xp": self.progression["xp"]
        }

    # =========================
    # SERIALIZATION
    # =========================
    def toDict(self):
        return {
            "playerId": self.playerId,
            "gold": self.core["gold"],
            "hp": self.core["hp"],
            "maxhp": self.core["maxHp"],
            "level": self.progression["level"],
            "xp": self.progression["xp"],
            "attack": self.combat["attack"],
            "defense": self.combat["defense"],
            "critchance": self.combat["critChance"],
            "critmultiplier": self.combat["critMultiplier"]
        }

    def getStats(self):
        return {
            "core": self.core,
            "progression": self.progression,
            "combat": self.combat
        }