from datetime import datetime, timezone
import asyncio


class GameEventService:
    def __init__(self, gameState, questManager, wsManager=None):
        self.gameState = gameState
        self.questManager = questManager
        self.wsManager = wsManager
        self.eventHistory = []

    def handleEvent(self, event):
        enrichedEvent = self._enrichEvent(event)
        self._storeEvent(enrichedEvent)

        eventType = enrichedEvent["type"]
        playerId = enrichedEvent["playerId"]
        data = enrichedEvent.get("data", {})

        player = self.gameState.getPlayer(playerId)
        if not player:
            return

        if eventType == "FIGHT_WIN":
            player.gainXP(data.get("xp", 0))
            player.core["gold"] += data.get("gold", 0)

        elif eventType == "FIGHT_LOSE":
            pass

        elif eventType in ("BUY", "SELL"):
            pass

        if eventType in ("FIGHT_WIN", "FIGHT_LOSE", "BUY", "SELL"):
            self._broadcastLeaderboard()

    # =========================================================
    # SAFE BROADCAST (TEST FRIENDLY)
    # =========================================================
    def _broadcastLeaderboard(self):
        if not self.wsManager:
            return

        game = self.gameState.getGameInstance()
        if not game:
            return

        payload = game.getLeaderboard()

        self._dispatchBroadcast(payload)

    def _dispatchBroadcast(self, payload):
        """
        Production: async
        Tests: runs sync (no event loop needed)
        """

        if asyncio.get_event_loop().is_running():
            # real server runtime
            asyncio.create_task(
                self.wsManager.broadcastLeaderboard(payload)
            )
        else:
            # test runtime (or sync context)
            coro = self.wsManager.broadcastLeaderboard(payload)
            asyncio.run(coro)

    # =========================================================
    # EVENT STORAGE
    # =========================================================
    def _storeEvent(self, event):
        self.eventHistory.append(event)

    def getEvents(self, limit=None):
        events = list(reversed(self.eventHistory))
        return events[:limit] if limit else events

    def _enrichEvent(self, event):
        return {
            "type": event["type"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "playerId": event["playerId"],
            "data": event.get("data", {}),
        }