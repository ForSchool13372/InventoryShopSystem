class Quest:
    def __init__(
        self,
        name,
        targetEnemy,
        target,
        rewardXP,
        rewardGold=0,
        progress=0,
        completed=False,
        unlocked=False,
        claimed=False
    ):
        self.name = name
        self.targetEnemy = targetEnemy.lower()
        self.target = target
        self.rewardXP = rewardXP
        self.rewardGold = rewardGold

        self.progress = progress
        self.completed = completed
        self.unlocked = unlocked
        self.claimed = claimed

    def getStatus(self):
        return {
            "name": self.name,
            "targetenemy": self.targetEnemy,
            "target": self.target,
            "progress": self.progress,
            "rewardxp": self.rewardXP,
            "rewardgold": self.rewardGold,
            "completed": self.completed,
            "unlocked": self.unlocked,
            "claimed": self.claimed
        }

    def complete(self):
        if self.completed:
            return False

        self.completed = True
        return True

    def update(self, enemyName):
        if self.completed or not self.unlocked or enemyName != self.targetEnemy:
            return False

        self.progress += 1

        if self.progress >= self.target:
            return self.complete()

        return False

    def claim(self):
        if not self.completed or self.claimed:
            return {
                "xp": 0,
                "gold": 0
            }

        self.claimed = True

        return {
            "xp": self.rewardXP,
            "gold": self.rewardGold
        }
