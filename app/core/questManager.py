class QuestManager:
    def __init__(self, quests, player):
        self.quests = quests
        self.player = player

    def update(self, enemyName):
        enemyName = enemyName.lower()

        for quest in self.quests:
            completedNow = quest.update(enemyName, self.player)

            if completedNow:
                self.unlockNextQuest(quest)

    def unlockNextQuest(self, quest):
        index = self.quests.index(quest)

        if index + 1 < len(self.quests):
            self.quests[index + 1].unlocked = True