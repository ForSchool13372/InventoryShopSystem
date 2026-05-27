from auth import createAccessToken

class Controller:
    def __init__(self, ctx):
        # =========================================================
        # CONTEXT
        # =========================================================
        self.ctx = ctx

        self.player = ctx.player
        self.playerId = ctx.playerId

        self.services = ctx.services
        self.repos = ctx.repos
        self.world = ctx.world

        self.questManager = ctx.questManager
        self.gameEventService = ctx.gameEventService

        # =========================================================
        # SHORTCUTS (CLEAN ACCESS)
        # =========================================================
        self.combatService = self.services.combat
        self.shopService = self.services.shop
        self.itemService = self.services.item

        self.shopRepo = self.repos.shop
        self.inventoryRepo = self.repos.inventory
        self.playerRepo = self.repos.player

    # =========================================================
    # AUTH / LIFECYCLE
    # =========================================================

    def login(self):
        return {
            "success": True,
            "token": createAccessToken({"playerId": self.playerId})
        }

    def revive(self):
        self.player.revive()

    def persist(self):
        self.playerRepo.save(self.playerId, self.player)

    # =========================================================
    # PLAYER INFO
    # =========================================================

    def getPlayerStats(self):
        return {
            "gold": self.player.gold,
            "hp": self.player.hp,
            "level": self.player.level,
            "xp": self.player.xp
        }

    # =========================================================
    # GAME ACTIONS
    # =========================================================

    def fight(self):
        result = self.combatService.handleFight(self.player, self.world.enemies)

        if result["result"] == "win":
            self.emitEvent({
                "type": "fightWin",
                "xp": result["xp"],
                "enemy": result["enemy"]
            })
        else:
            self.emitEvent({"type": "fightLose"})

        return result

    def buy(self, itemName, quantity):
        item = self.itemService.getItem(itemName.lower())

        return self.shopService.buy(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    def sell(self, itemName, quantity):
        item = self.itemService.getItem(itemName.lower())

        return self.shopService.sell(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    # =========================================================
    # DATA ACCESS
    # =========================================================

    def getShop(self):
        return self.shopRepo.getShopItems()

    def getInventory(self):
        return self.inventoryRepo.loadInventory(self.playerId)

    def getQuests(self):
        return self.world.quests

    # =========================================================
    # INTERNAL EVENTS
    # =========================================================

    def emitEvent(self, event):
        self.gameEventService.handleEvent(event)