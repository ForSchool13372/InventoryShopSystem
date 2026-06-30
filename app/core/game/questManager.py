class QuestManager:
    def __init__(self, quests, player, questRepo):
        self.quests = quests
        self.player = player
        self.questRepo = questRepo

    # =========================================================
    # UPDATE QUEST PROGRESS
    # =========================================================
    def update(self, enemyName: str):
        enemyName = enemyName.lower()

        completedQuests = []

        for quest in self.quests:
            if quest.update(enemyName):
                completedQuests.append({
                    "name": quest.name,
                    "rewardXp": quest.rewardXP,
                    "rewardGold": quest.rewardGold
                })
                self.unlockNextQuest(quest)

        return {
            "completed": completedQuests
        }

    # =========================================================
    # UNLOCK NEXT QUEST
    # =========================================================
    def unlockNextQuest(self, quest):
        index = self.quests.index(quest)

        if index + 1 < len(self.quests):
            self.quests[index + 1].unlocked = True

    # =========================================================
    # CLAIM QUEST
    # =========================================================
    def claimQuest(self, quest):
        # already claimed
        if quest.claimed:
            return {
                "state": "already_claimed",
                "xp": 0,
                "gold": 0
            }

        # not completed yet
        if not quest.completed:
            return {
                "state": "not_completed",
                "xp": 0,
                "gold": 0
            }

        result = quest.claim()

        if result["xp"] <= 0 and result["gold"] <= 0:
            return {
                "state": "not_completed",
                "xp": 0,
                "gold": 0
            }

        quest.claimed = True

        return {
            "state": "claimed",
            "xp": result["xp"],
            "gold": result["gold"]
        }

