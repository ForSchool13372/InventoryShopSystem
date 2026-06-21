from typing import Dict, Any
from app.core.auth import createAccessToken
from app.state.gameState import gameState
from app.core.gameFactory import PlayerFactory


class Controller:
    def __init__(self, ctx):
        self.ctx = ctx
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
    # HELPERS
    # =========================================================
    def _getPlayer(self):
        return gameState.getPlayer(self.playerId)

    # =========================================================
    # LIFECYCLE
    # =========================================================
    def login(self) -> Dict[str, Any]:
        data = self.playerRepo.load(self.playerId)

        if not data:
            return {"success": False, "message": "Player not found"}

        player = PlayerFactory.fromData(data)
        gameState.addPlayer(self.playerId, player)

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
        player = self._getPlayer()
        if not player:
            return {"success": False}

        player.revive()
        self._emitEvent("REVIVE")
        return {"success": True}

    # =========================================================
    # PLAYER
    # =========================================================
    def getPlayerStats(self) -> Dict[str, Any]:
        player = self._getPlayer()

        if not player:
            return {
                "gold": 0,
                "hp": 100,
                "level": 1,
                "xp": 0
            }

        return player.getStats()

    # =========================================================
    # GAME ACTIONS
    # =========================================================
    def fight(self) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        result = self.combat.handleFight(player, self.world.enemies)

        eventType = (
            "FIGHT_WIN"
            if result and result.get("result") == "win"
            else "FIGHT_LOSE"
        )

        self._emitEvent(eventType, {
            "xp": result.get("xp") if result else None,
            "enemy": result.get("enemy") if result else None
        })

        self.playerRepo.save(self.playerId, player)

        return result

    def buy(self, itemName: str, quantity: int) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        item = self.items.getItem(itemName)
        if not item:
            return {"success": False, "message": "Item not found"}

        ctx = self._buildShopCtx(player, item, quantity)
        result = self.shop.buy(ctx)

        self.playerRepo.save(self.playerId, player)

        self._emitEvent("BUY", {
            "item": itemName,
            "quantity": quantity
        })

        return result

    def sell(self, itemName: str, quantity: int) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        item = self.items.getItem(itemName)
        if not item:
            return {"success": False, "message": "Item not found"}

        ctx = self._buildShopCtx(player, item, quantity)
        result = self.shop.sell(ctx)

        self.playerRepo.save(self.playerId, player)

        self._emitEvent("SELL", {
            "item": itemName,
            "quantity": quantity
        })

        return result

    # =========================================================
    # DATA ACCESS
    # =========================================================
    def getShop(self) -> Any:
        return self.shopRepo.getShopStock()

    def getInventory(self) -> Any:
        return self.inventoryRepo.loadInventory(self.playerId)

    def getQuests(self) -> Any:
        return self.world.quests

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================
    def _buildShopCtx(self, player, item, quantity):
        class ShopCtx:
            pass

        ctx = ShopCtx()
        ctx.player = player
        ctx.playerId = self.playerId
        ctx.item = item
        ctx.quantity = quantity
        ctx.shopRepo = self.shopRepo

        return ctx