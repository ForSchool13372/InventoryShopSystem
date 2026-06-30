class Player:
    def __init__(
        self,
        playerId: int,
        gold: int = 0,
        hp: int = 100,
        maxhp: int = 100,
        level: int = 1,
        xp: int = 0
    ):
        self.playerId = playerId

        # =========================
        # CORE
        # =========================
        self.core = {
            "gold": gold or 0,
            "hp": hp or 100,
            "maxhp": maxhp or 100
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
            "critchance": 0.05,
            "critmultiplier": 1.5
        }

        self.clampHp()

    # =========================
    # HP SYSTEM
    # =========================
    def clampHp(self):
        hp = self.core.get("hp") or 0
        maxhp = self.core.get("maxhp") or 100

        self.core["hp"] = max(0, min(hp, maxhp))
        self.core["maxhp"] = maxhp

    def isDead(self):
        return self.core["hp"] <= 0

    def revive(self):
        self.core["hp"] = self.core["maxhp"]

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

            self.core["maxhp"] += 10
            self.core["hp"] = min(
                self.core["maxhp"],
                self.core["hp"] + self.core["maxhp"] // 2
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
            "maxhp": self.core["maxhp"],
            "level": self.progression["level"],
            "xp": self.progression["xp"],
            "attack": self.combat["attack"],
            "defense": self.combat["defense"],
            "critchance": self.combat["critchance"],
            "critmultiplier": self.combat["critmultiplier"]
        }

    def getStats(self):
        return {
            "core": self.core,
            "progression": self.progression,
            "combat": self.combat
        }