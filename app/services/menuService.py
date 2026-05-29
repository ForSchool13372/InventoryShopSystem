class MenuService:
    def __init__(self, shopRepo):
        self.shopRepo = shopRepo

    def getBuyInput(self):
        itemName = input("Enter item name: ")

        while True:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be > 0")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")

        return itemName, quantity

    def getSellInput(self):
        itemName = input("Enter item name: ")

        while True:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be > 0")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")

        return itemName, quantity

    def showStock(self):
        rows = self.shopRepo.getShopStock()
        for r in rows:
            print(r["itemName"], "x", r["stock"])

    def showInventory(self, items):
        print(items)

    def getBuyFlow(self):
        self.showStock()
        return self.getBuyInput()

    def getSellFlow(self):
        return self.getSellInput()

    def getChoice(self):
        return input("> ")