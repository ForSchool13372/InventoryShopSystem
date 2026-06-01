from app.models.enemy import Enemy
from app.models.quest import Quest
from app.models.item import Item

def createItems():
    #Dictionary
    return {
        "sword": Item("sword", 20),
        "potion": Item("potion", 5),
        "garbage": Item("garbage", 5)
        }

def createEnemies():
    #List
    return [
        Enemy("Training Dummy", 50, 30, 2, 5),
        Enemy("Goblin", 70, 50, 4, 10),
        Enemy("Slime", 40, 20, 1, 3)
    ]

def createQuests():
    quests = [
        Quest("Kill Slimes", "slime", 3,50),
        Quest("Kill Goblins", "goblin", 2, 80)
        ]
    quests[0].unlocked = True
    return quests

def seedShop(shop):
    items = createItems()
    shop.addItemToStock(items["sword"], 5)
    shop.addItemToStock(items["potion"], 15)
    shop.addItemToStock(items["garbage"], 10)
