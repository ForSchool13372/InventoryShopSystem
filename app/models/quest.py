class Quest:
    def __init__(self, name, targetEnemy, target, rewardXP):
        self.name = name
        self.targetEnemy = targetEnemy.lower()
        self.target = target
        self.progress = 0
        self.rewardXP = rewardXP
        self.completed = False
        self.unlocked = False

    def getStatus(self):
        return {
            "name": self.name,
            "progress": self.progress,
            "target": self.target,
            "rewardXP": self.rewardXP,
            "completed": self.completed,
            "unlocked": self.unlocked
        }

    def complete(self):
        if self.completed:
            return 0

        self.completed = True
        return self.rewardXP

    def update(self, enemyName):
        if self.completed or not self.unlocked or enemyName != self.targetEnemy:
            return 0

        self.progress += 1

        if self.progress >= self.target:
            return self.complete()

        return 0