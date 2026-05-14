class MenuService:
    def __init__(self, controller):
        self.controller = controller

    def getActions(self):
        return {
            "1": self.controller.handleBuy,
            "2": self.controller.handleSell,
            "3": self.controller.handleInventory,
            "4": self.controller.handleStats,
            "5": self.controller.handleFight,
            "6": self.controller.handleExit,
            "7": self.controller.handleQuest,
            }

    def getBuyInput(self):
        itemName = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        return itemName, quantity

    def getSellInput(self):
        itemName = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        return itemName, quantity