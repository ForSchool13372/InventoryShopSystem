from datetime import datetime, timezone


class GameEventService:
    def __init__(self, gameState, questManager):
        self.gameState = gameState
        self.questManager = questManager
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

        # =========================================================
        # GAME LOGIC
        # =========================================================

        if eventType == "FIGHT_WIN":
            player.gainXP(enrichedEvent.get("xp", 0))
            self.questManager.update(enrichedEvent.get("enemy"))

        elif eventType == "FIGHT_LOSE":
            player.hp = 0

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