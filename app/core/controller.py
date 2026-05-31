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
        token = createAccessToken({
            "playerId": self.playerId
        })

        return {
            "success": True,
            "token": token
        }

    def revive(self):
        self.player.revive()
        return {"success": True}

    def persist(self):
        self.playerRepo.save(self.playerId, self.player)
        return {"success": True}

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
        ctx = self._buildShopCtx(item, quantity)
        return self.shop.buy(ctx)

    def sell(self, itemName, quantity):
        item = self.items.getItem(itemName)
        ctx = self._buildShopCtx(item, quantity)
        return self.shop.sell(ctx)

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

    def _buildShopCtx(self, item, quantity):
        ctx = type("Ctx", (), {})()
        ctx.player = self.player
        ctx.playerId = self.playerId
        ctx.item = item
        ctx.quantity = quantity
        ctx.shopRepo = self.shopRepo
        return ctx

    def _handle_fight_events(self, result):
        event_type = "fightWin" if result.get("result") == "win" else "fightLose"

        payload = {"type": event_type}

        if event_type == "fightWin":
            payload["xp"] = result.get("xp")
            payload["enemy"] = result.get("enemy")

        self.gameEventService.handleEvent(payload)