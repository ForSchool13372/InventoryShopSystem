from types import SimpleNamespace

class FakeCombat:
    def handleFight(self, player, enemies):
        return {"result": "win", "enemy": SimpleNamespace(name="goblin")}


class FakeShop:
    def buy(self, ctx):
        return {"cost": 10, "enemy": None}

    def sell(self, ctx):
        return {"gain": 5}


class FakeItemService:
    def getItem(self, name):
        return SimpleNamespace(name=name, price=10)


class FakeLoot:
    def generateLoot(self, enemy):
        return [{"itemName": "potion", "qty": 1}]


class FakeInventory:
    def addItems(self, playerId, items):
        pass


class FakeLeaderboard:
    def getLeaderboard(self):
        return []


class FakeEventService:
    def handleEvent(self, event):
        pass


class FakeRNG:
    def randint(self, a, b):
        return 10

    def choice(self, items):
        return items[0]