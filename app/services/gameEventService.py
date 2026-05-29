class GameEventService:
    def __init__(self, player, questManager):
        self.player = player
        self.questManager = questManager

    def handleEvent(self, event):
        eventType = event["type"]

        if eventType == "fightWin":
            self.player.gainXP(event["xp"])
            self.questManager.update(event["enemy"])

        elif eventType == "fightLose":
            self.player.hp = 0