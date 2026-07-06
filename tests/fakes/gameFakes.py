from types import SimpleNamespace


# =========================================================
# COMBAT
# =========================================================

class FakeCombat:
    def handleFight(self, player, enemies):
        return {
            "result": "win",
            "enemy": SimpleNamespace(name="goblin")
        }


# =========================================================
# SHOP (NO MISSING BRANCHES)
# =========================================================

class FakeShop:
    def buy(self, ctx):
        return {
            "cost": 10,
            "enemy": None
        }

    def sell(self, ctx):
        return {
            "gain": 5
        }


# =========================================================
# ITEM SERVICE (IMPORTANT: missing-item branch support)
# =========================================================

class FakeItemService:
    def __init__(self):
        self.items = {
            "sword": SimpleNamespace(name="sword", price=10)
        }

    def getItem(self, name):
        return self.items.get(name, None)


# =========================================================
# LOOT
# =========================================================

class FakeLoot:
    def generateLoot(self, enemy):
        return [
            {"itemName": "potion", "qty": 1}
        ]


# =========================================================
# INVENTORY
# =========================================================

class FakeInventory:
    def __init__(self):
        self.items = []

    def addItems(self, playerId, items):
        self.items.extend(items)


# =========================================================
# LEADERBOARD
# =========================================================

class FakeLeaderboard:
    def getLeaderboard(self):
        return [
            {"playerId": 1, "score": 100}
        ]


# =========================================================
# EVENT SERVICE
# =========================================================

class FakeEventService:
    def __init__(self):
        self.events = []

    def handleEvent(self, event):
        self.events.append(event)


# =========================================================
# RNG (SAFE DEFAULT)
# =========================================================

class FakeRNG:
    def randint(self, a, b):
        return a

    def choice(self, items):
        return items[0]