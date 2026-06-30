from app.services.inventoryService import InventoryService

class FakeInventoryRepo:
    def __init__(self):
        self.inventory = []

    def loadInventory(self, playerId):
        return self.inventory

    def saveInventory(self, playerId, inventoryDict):
        self.savedPlayerId = playerId
        self.savedInventory = inventoryDict


def test_addItems_adds_new_items():
    repo = FakeInventoryRepo()
    service = InventoryService(repo)

    service.addItems(
        1,
        [
            {"itemName": "Potion", "qty": 2},
            {"itemName": "Sword", "qty": 1},
        ],
    )

    assert repo.savedInventory == {
        "Potion": 2,
        "Sword": 1,
    }


def test_addItems_stacks_existing_items():
    repo = FakeInventoryRepo()
    repo.inventory = [
        {"itemName": "Potion", "quantity": 3},
    ]

    service = InventoryService(repo)

    service.addItems(
        1,
        [
            {"itemName": "Potion", "qty": 2},
        ],
    )

    assert repo.savedInventory == {
        "Potion": 5,
    }


def test_addItems_with_empty_list_does_nothing():
    repo = FakeInventoryRepo()
    service = InventoryService(repo)

    service.addItems(1, [])

    assert not hasattr(repo, "savedInventory")