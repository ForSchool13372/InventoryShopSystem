from app.core.auth import createAccessToken

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
        # SHORTCUTS
        # =========================================================
        self.combat = self.services.combat
        self.shop = self.services.shop
        self.items = self.services.item

        self.shopRepo = self.repos.shop
        self.inventoryRepo = self.repos.inventory
        self.playerRepo = self.repos.player

    # =========================================================
    # LIFECYCLE
    # =========================================================

    def login(self):
        print("PLAYER ID:", self.playerId)

        token = createAccessToken({
            "playerId": self.playerId
        })

        return {
            "success": True,
            "token": token
        }

    def revive(self):
        self.player.revive()

    def persist(self):
        self.playerRepo.save(self.playerId, self.player)

    # =========================================================
    # PLAYER
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
        result = self.combat.handleFight(self.player, self.world.enemies)

        self._handle_fight_events(result)

        return result

    def buy(self, itemName, quantity):
        item = self.items.getItem(itemName)

        return self.shop.buy(
            self.player,
            item,
            quantity,
            self.playerId,
            self.shopRepo
        )

    def sell(self, itemName, quantity):
        item = self.items.getItem(itemName)

        return self.shop.sell(
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
    # INTERNAL HELPERS
    # =========================================================

    def _handle_fight_events(self, result):
        if result["result"] == "win":
            self.gameEventService.handleEvent({
                "type": "fightWin",
                "xp": result.get("xp"),
                "enemy": result.get("enemy")
            })
        else:
            self.gameEventService.handleEvent({
                "type": "fightLose"
            })