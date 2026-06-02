from datetime import datetime, timezone


class GameEventService:
    def __init__(self, player, questManager):
        self.player = player
        self.questManager = questManager

        # =========================================================
        # EVENT HISTORY (HIGH ROI ADDITION)
        # =========================================================
        self.eventHistory = []

    # =========================================================
    # PUBLIC API
    # =========================================================

    def handleEvent(self, event):
        """
        Processes game events + stores history for later retrieval
        """

        enrichedEvent = self._enrichEvent(event)
        self._storeEvent(enrichedEvent)

        eventType = enrichedEvent["type"]

        # =========================================================
        # GAME LOGIC
        # =========================================================

        if eventType == "fightWin":
            self.player.gainXP(enrichedEvent["xp"])
            self.questManager.update(enrichedEvent["enemy"])

        elif eventType == "fightLose":
            self.player.hp = 0

    # =========================================================
    # EVENT STORAGE
    # =========================================================

    def _storeEvent(self, event):
        self.eventHistory.append(event)

    def getEvents(self, limit=None):
        """
        Returns event history (latest first)
        """
        events = list(reversed(self.eventHistory))

        if limit:
            return events[:limit]

        return events

    # =========================================================
    # EVENT ENRICHMENT
    # =========================================================

    def _enrichEvent(self, event):
        """
        Adds metadata to every event (VERY IMPORTANT FOR PORTFOLIO)
        """

        return {
            "type": event["type"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "playerId": getattr(self.player, "id", None),
            **event
        }