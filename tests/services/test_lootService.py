from app.services.lootService import LootService


# =========================================================
# FAKE RANDOM (CONTROLLED OUTPUT)
# =========================================================

class FakeRandom:
    def __init__(self, randint_value, choice_values):
        self.randint_value = randint_value
        self.choice_values = choice_values
        self.choice_index = 0

    def randint(self, a, b):
        return self.randint_value

    def choice(self, pool):
        # cycle through predefined values
        value = self.choice_values[self.choice_index % len(self.choice_values)]
        self.choice_index += 1
        return value


# =========================================================
# TESTS
# =========================================================

def test_goblin_drops_fixed_items(monkeypatch):
    service = LootService()

    fake_random = FakeRandom(
        randint_value=2,  # always drop 2 items
        choice_values=["potion", "garbage"]
    )

    monkeypatch.setattr("app.services.lootService.random", fake_random)

    enemy = type("Enemy", (), {"name": "goblin"})()

    loot = service.generateLoot(enemy)

    assert len(loot) == 2
    assert sorted([item["itemName"] for item in loot]) in [
        ["garbage", "potion"],
        ["potion", "potion"],
        ["garbage", "garbage"]
    ]


def test_training_dummy_always_garbage(monkeypatch):
    service = LootService()

    fake_random = FakeRandom(
        randint_value=1,
        choice_values=["garbage"]
    )

    monkeypatch.setattr("app.services.lootService.random", fake_random)

    enemy = type("Enemy", (), {"name": "training dummy"})()

    loot = service.generateLoot(enemy)

    assert all(item["itemName"] == "garbage" for item in loot)


def test_zero_drop(monkeypatch):
    service = LootService()

    fake_random = FakeRandom(
        randint_value=0,
        choice_values=[]
    )

    monkeypatch.setattr("app.services.lootService.random", fake_random)

    enemy = type("Enemy", (), {"name": "orc"})()

    loot = service.generateLoot(enemy)

    assert loot == []