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

        # FIGHT WIN
        if eventType == "FIGHT_WIN":
            player.gainXP(data.get("xp", 0))
            player.core["gold"] += data.get("gold", 0)

        # FIGHT LOSE
        elif eventType == "FIGHT_LOSE":
            pass

        # BUY / SELL
        elif eventType in ("BUY", "SELL"):
            pass

        if eventType in ("FIGHT_WIN", "FIGHT_LOSE", "BUY", "SELL"):
            self._broadcastLeaderboard()

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

    def _broadcastLeaderboard(self):
        if not self.wsManager:
            return

        game = self.gameState.getGameInstance()
        if not game:
            return

        asyncio.create_task(
            self.wsManager.broadcastLeaderboard(
                game.getLeaderboard()
            )
        )