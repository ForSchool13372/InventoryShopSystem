from typing import Dict, Any
from app.core.auth import createAccessToken


class Controller:
    def __init__(self, ctx):
        self.ctx = ctx
        self.player = ctx.player
        self.playerId = ctx.playerId

        self.services = ctx.services
        self.repos = ctx.repos
        self.world = ctx.world

        self.questManager = ctx.questManager
        self.gameEventService = ctx.gameEventService

        self.combat = self.services.combat
        self.shop = self.services.shop
        self.items = self.services.item

        self.shopRepo = self.repos.shop
        self.inventoryRepo = self.repos.inventory
        self.playerRepo = self.repos.player

    # =========================================================
    # EVENT SYSTEM
    # =========================================================
    def _emitEvent(self, eventType: str, data: Dict[str, Any] = None) -> None:
        try:
            self.gameEventService.handleEvent({
                "type": eventType,
                "playerId": self.playerId,
                "data": data or {}
            })
        except Exception:
            pass

    # =========================================================
    # LIFECYCLE
    # =========================================================
    def login(self) -> Dict[str, Any]:
        token: str = createAccessToken({
            "playerId": self.playerId
        })

        self._emitEvent("LOGIN")

        return {
            "success": True,
            "id": self.playerId,
            "token": token
        }

    def revive(self) -> Dict[str, Any]:
        self.player.revive()
        self._emitEvent("REVIVE")
        return {"success": True}

    def persist(self) -> Dict[str, Any]:
        self.playerRepo.save(self.playerId, self.player)
        return {"success": True}

    # =========================================================
    # PLAYER
    # =========================================================
    def getPlayerStats(self) -> Dict[str, Any]:
        return {
            "gold": self.player.gold,
            "hp": self.player.hp,
            "level": self.player.level,
            "xp": self.player.xp
        }

    # =========================================================
    # GAME ACTIONS
    # =========================================================
    def fight(self) -> Dict[str, Any]:
        result = self.combat.handleFight(self.player, self.world.enemies)

        eventType = (
            "FIGHT_WIN"
            if result and result.get("result") == "win"
            else "FIGHT_LOSE"
        )

        self._emitEvent(eventType, {
            "xp": result.get("xp") if result else None,
            "enemy": result.get("enemy") if result else None
        })

        return result

    def buy(self, itemName: str, quantity: int) -> Dict[str, Any]:
        item = self.items.getItem(itemName)

        if not item:
            return {"success": False, "message": "Item not found"}

        ctx = self._buildShopCtx(item, quantity)
        result = self.shop.buy(ctx)

        self._emitEvent("BUY", {
            "item": itemName,
            "quantity": quantity
        })

        return result

    def sell(self, itemName: str, quantity: int) -> Dict[str, Any]:
        item = self.items.getItem(itemName)

        if not item:
            return {"success": False, "message": "Item not found"}

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
    def getShop(self) -> Any:
        return self.shopRepo.getShopItems()

    def getInventory(self) -> Any:
        return self.inventoryRepo.loadInventory(self.playerId)

    def getQuests(self) -> Any:
        return self.world.quests

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================
    def _buildShopCtx(self, item, quantity):
        class ShopCtx:
            pass

        ctx = ShopCtx()
        ctx.player = self.player
        ctx.playerId = self.playerId
        ctx.item = item
        ctx.quantity = quantity
        ctx.shopRepo = self.shopRepo

        return ctx