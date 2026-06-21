from datetime import datetime, timezone
import asyncio


class GameEventService:
    def __init__(self, gameState, questManager, wsManager=None):
        self.gameState = gameState
        self.questManager = questManager
        self.wsManager = wsManager
        self.eventHistory = []

    # =========================================================
    # PUBLIC API
    # =========================================================
    def handleEvent(self, event):
        enrichedEvent = self._enrichEvent(event)
        self._storeEvent(enrichedEvent)

        eventType = enrichedEvent["type"]
        playerId = enrichedEvent["playerId"]

        player = self.gameState.getPlayer(playerId)

        if not player:
            return

        data = enrichedEvent.get("data", {})

        # =========================================================
        # GAME LOGIC
        # =========================================================

        if eventType == "FIGHT_WIN":
            player.gainXP(data.get("xp", 0))

            player.core["gold"] += data.get("gold", 0)

            self.questManager.update(data.get("enemy"))
            self._broadcastLeaderboard()

        elif eventType == "FIGHT_LOSE":
            player.core["hp"] = 0
            self._broadcastLeaderboard()

    # =========================================================
    # EVENT STORAGE
    # =========================================================
    def _storeEvent(self, event):
        self.eventHistory.append(event)

    def getEvents(self, limit=None):
        events = list(reversed(self.eventHistory))
        return events[:limit] if limit else events

    # =========================================================
    # EVENT ENRICHMENT
    # =========================================================
    def _enrichEvent(self, event):
        return {
            "type": event["type"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "playerId": event["playerId"],
            "data": event.get("data", {}),
        }

    # =========================================================
    # WS INTEGRATION
    # =========================================================
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