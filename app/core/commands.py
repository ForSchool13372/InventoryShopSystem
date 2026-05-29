class BuyCommand:
    def __init__(self, menuService):
        self.menuService = menuService

    def execute(self):
        self.menuService.handleShopBuyFlow()

class SellCommand:
    def __init__(self, menuService):
        self.menuService = menuService

    def execute(self):
        self.menuService.handleShopSellFlow()
