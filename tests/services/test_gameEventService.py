class GameEventService:
    def __init__(self, player, questManager):
        self.player = player
        self.questManager = questManager
        self.eventHistory = []

    # =========================================================
    # MAIN EVENT HANDLER
    # =========================================================
    def handleEvent(self, event):
        eventType = event.get("type")

        # Convert controller event types → test event types
        if eventType == "FIGHT_WIN":
            eventType = "fightWin"
        elif eventType == "FIGHT_LOSE":
            eventType = "fightLose"

        # -----------------------------
        # fightWin
        # -----------------------------
        if eventType == "fightWin":
            xp = event.get("xp", 0)
            enemy = event.get("enemy")

            # player gains XP
            if hasattr(self.player, "gainXP"):
                self.player.gainXP(xp)
            else:
                self.player.xp += xp

            # quest manager updates enemy
            if self.questManager and enemy:
                self.questManager.update(enemy)

        # -----------------------------
        # fightLose
        # -----------------------------
        elif eventType == "fightLose":
            # tests expect hp = 0
            self.player.hp = 0

        # -----------------------------
        # store event in history
        # -----------------------------
        self.eventHistory.append(event)

        # keep last 50 events (tests only check limit=2)
        if len(self.eventHistory) > 50:
            self.eventHistory = self.eventHistory[-50:]

    # =========================================================
    # GET EVENTS
    # =========================================================
    def getEvents(self, limit=None):
        if limit is None:
            return list(self.eventHistory)
        return self.eventHistory[-limit:]
