from inventory import Inventory

class Player:
    def __init__(self, gold):
        self.gold = gold
        self.inventory = Inventory()

        #XP System
        self.level = 1
        self.xp = 0

        #Combat system
        self.hp = 100

    def takeDamage(self, damage):
        self.hp = max(0, self.hp - damage)

    def gainXP(self, amount):
        #Add xp to player (Progression system starts here)
        self.xp += amount
        print(f"+{amount} XP | {self.xp}/100")

        #Check if player should level up
        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            print("Level Up! Now level", self.level)

    #Convert player state to dict for saving
    def toDict(self):
        return {
            "gold": self.gold,
            "inventory": self.inventory.items
            }

    #Show stats method
    def showStats(self):
        print("Gold:",self.gold)
        print("Level:",self.level)
        print(f"XP: {self.xp}/100")
        print("HP:",self.hp)

    def revive(self):
        self.hp = 100