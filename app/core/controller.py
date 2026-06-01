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
    # EVENT SYSTEM (HIGH ROI ADDITION)
    # =========================================================

    def _emitEvent(self, eventType, data=None):
        """
        Centralized event logging system
        """
        payload = {
            "type": eventType,
            "playerId": self.playerId,
            "data": data or {}
        }

        self.gameEventService.handleEvent(payload)

    # =========================================================
    # LIFECYCLE
    # =========================================================

    def login(self):
        token = createAccessToken({
            "playerId": self.playerId
        })

        self._emitEvent("LOGIN")

        return {
            "success": True,
            "token": token
        }

    def revive(self):
        self.player.revive()

        self._emitEvent("REVIVE")

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

        eventType = "FIGHT_WIN" if result.get("result") == "win" else "FIGHT_LOSE"

        self._emitEvent(eventType, {
            "xp": result.get("xp"),
            "enemy": result.get("enemy")
        })

        return result

    def buy(self, itemName, quantity):
        item = self.items.getItem(itemName)
        ctx = self._buildShopCtx(item, quantity)

        result = self.shop.buy(ctx)

        self._emitEvent("BUY", {
            "item": itemName,
            "quantity": quantity
        })

        return result

    def sell(self, itemName, quantity):
        item = self.items.getItem(itemName)
        ctx = self._buildShopCtx(item, quantity)

        result = self.shop.sell(ctx)

        self._emitEvent("SELL", {
            "item": itemName,
            "quantity": quantity
        })

        return result

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