from typing import Dict, Any
from app.core.auth import createAccessToken
from app.state.gameState import gameState
from app.core.game.gameFactory import PlayerFactory
from app.core.wsManager import wsManager
from app.core.game.seed import createEnemies


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

        self.loot = self.services.loot
        self.inventoryService = self.services.inventory

        self.shopRepo = self.repos.shop
        self.inventoryRepo = self.repos.inventory
        self.playerRepo = self.repos.player

        self.leaderboardService = self.services.leaderboard

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _syncPlayer(self):
        data = self.playerRepo.load(self.playerId)
        if not data:
            return

        player = PlayerFactory.fromData(self.playerId, data)
        gameState.updatePlayer(self.playerId, player)

    def _emitEvent(self, eventType: str, data: Dict[str, Any] = None) -> None:
        try:
            self.gameEventService.handleEvent({
                "type": eventType,
                "playerId": self.playerId,
                "data": data or {}
            })
        except Exception:
            pass

    def _getPlayer(self):
        player = gameState.getPlayer(self.playerId)

        if player is None:
            data = self.playerRepo.load(self.playerId)
            if not data:
                return None

            player = PlayerFactory.fromData(self.playerId, data)
            gameState.addPlayer(self.playerId, player)

        return player

    # =========================================================
    # LOGIN
    # =========================================================
    def login(self) -> Dict[str, Any]:
        data = self.playerRepo.load(self.playerId)

        if not data:
            data = {
                "gold": 0,
                "hp": 100,
                "maxhp": 100,
                "level": 1,
                "xp": 0,
                "attack": 10,
                "defense": 5,
                "critchance": 0.05,
                "critmultiplier": 1.5
            }

        player = PlayerFactory.fromData(self.playerId, data)
        gameState.addPlayer(self.playerId, player)

        token = createAccessToken({"playerId": self.playerId})

        self._emitEvent("LOGIN")

        return {
            "success": True,
            "id": self.playerId,
            "token": token
        }

    # =========================================================
    # REVIVE
    # =========================================================

    def revive(self) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        player.revive()
        self._emitEvent("REVIVE")

        self.playerRepo.save(self.playerId, player)
        self._syncPlayer()

        return {"success": True}

    # =========================================================
    # PLAYER STATS
    # =========================================================

    def getPlayerStats(self) -> Dict[str, Any]:
        player = self._getPlayer()

        if not player:
            return {
                "core": {
                    "gold": 0,
                    "hp": 100,
                    "maxhp": 100
                },
                "progression": {
                    "level": 1,
                    "xp": 0
                },
                "combat": {
                    "attack": 10,
                    "defense": 5,
                    "critchance": 0.05,
                    "critmultiplier": 1.5
                }
            }

        return player.getStats()

    # =========================================================
    # FIGHT
    # =========================================================
    async def fight(self) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        result = self.combat.handleFight(player, createEnemies())

        enemy = result["enemy"]

        if result["result"] == "win":
            self.questManager.update(enemy.name)
            self.repos.quest.saveQuests(
                self.playerId,
                self.questManager.quests
            )

            loot = self.loot.generateLoot(enemy)
            self.inventoryService.addItems(self.playerId, loot)
            result["items"] = loot

        eventType = (
            "FIGHT_WIN"
            if result and result.get("result") == "win"
            else "FIGHT_LOSE"
        )

        self._emitEvent(eventType, result)

        self.playerRepo.save(self.playerId, player)

        await wsManager.broadcastLeaderboard(
            self.leaderboardService.getLeaderboard()
        )

        result["enemy"] = {
            "name": enemy.name,
            "startingHp": result["startingHp"],
            "finalHp": result["finalHp"],
            "maxHp": enemy.maxHp,
            "minDamage": enemy.minDamage,
            "maxDamage": enemy.maxDamage,
            "attack": enemy.attack,
            "xp": enemy.xp,
            "gold": enemy.gold
        }

        return result


    # =========================================================
    # BUY
    # =========================================================

    async def buy(self, itemName: str, quantity: int) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        item = self.items.getItem(itemName)
        if not item:
            return {"success": False, "message": "Item not found"}

        ctx = self._buildShopCtx(player, item, quantity)

        result = self.shop.buy(ctx)

        self._syncPlayer()

        self._emitEvent("BUY", {
            "item": itemName,
            "quantity": quantity,
            "cost": result.get("cost")
        })

        await wsManager.broadcastLeaderboard(
            self.leaderboardService.getLeaderboard()
        )

        enemy_obj = result.get("enemy")
        result["enemy"] = enemy_obj.toDict() if enemy_obj else None

        return result


    # =========================================================
    # SELL
    # =========================================================

    async def sell(self, itemName: str, quantity: int) -> Dict[str, Any]:
        player = self._getPlayer()
        if not player:
            return {"success": False}

        item = self.items.getItem(itemName)
        if not item:
            return {"success": False, "message": "Item not found"}

        ctx = self._buildShopCtx(player, item, quantity)

        result = self.shop.sell(ctx)

        self._syncPlayer()

        self._emitEvent("SELL", {
            "item": itemName,
            "quantity": quantity,
            "gain": result.get("gain")
        })

        await wsManager.broadcastLeaderboard(
            self.leaderboardService.getLeaderboard()
        )

        return result

    # =========================================================
    # QUEST
    # =========================================================

    async def claimQuest(self, questName):
        quest = next(
            (q for q in self.ctx.questManager.quests if q.name == questName),
            None
        )

        if not quest:
            return {"error": "Quest not found"}

        # apply quest logic
        result = self.ctx.questManager.claimQuest(quest)

        # =========================
        # APPLY REWARDS (CONTROLLER OWNS THIS)
        # =========================
        player = self._getPlayer()
        player.gainXP(result.get("xp", 0))
        player.core["gold"] += result.get("gold", 0)

        # persist quest state
        self.repos.quest.saveQuests(self.playerId, self.ctx.questManager.quests)

        # persist player state
        self.playerRepo.save(self.playerId, player)

        # sync cache/state
        self._syncPlayer()

        # async leaderboard update
        await wsManager.broadcastLeaderboard(
            self.leaderboardService.getLeaderboard()
        )

        return {
            "success": True,
            "rewards": {
                "xp": result.get("xp", 0),
                "gold": result.get("gold", 0)
            },
            "quest": {
                "completed": quest.completed,
                "claimed": quest.claimed
            }
        }

    # =========================================================
    # OTHER
    # =========================================================

    def getShop(self):
        return self.shopRepo.getShopStock()

    def getInventory(self):
        return self.inventoryRepo.loadInventory(self.playerId)

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