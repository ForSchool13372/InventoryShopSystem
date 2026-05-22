from shopService import ShopService
from shopRepository import ShopRepository
from inventoryRepository import InventoryRepository
from itemService import ItemService
from combatService import CombatService
from gameData import createEnemies, createQuests
from controller import Controller


class GameFactory:
    def __init__(self):
        self.shopService = ShopService()
        self.shopRepo = ShopRepository()
        self.inventoryRepo = InventoryRepository()
        self.itemService = ItemService()

        self.combatService = CombatService()
        self.enemies = createEnemies()
        self.quests = createQuests()

    def create(self, playerId):
        return Controller(
            playerId,
            self.shopService,
            self.shopRepo,
            self.inventoryRepo,
            self.itemService,
            self.combatService,
            self.enemies,
            self.quests
        )