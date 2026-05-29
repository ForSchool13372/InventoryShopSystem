from app.models.player import Player

class Quest:
    def __init__(self, name, targetEnemy, target, rewardXP):
        self.name = name
        self.targetEnemy = targetEnemy.lower()
        self.target = target
        self.progress = 0
        self.rewardXP = rewardXP
        self.completed = False
        self.unlocked = False

    def showQuest(self):
        print(f"\nQuest: {self.name}")
        print(f"Progress: {self.progress}/{self.target}")
        print(f"Reward: {self.rewardXP} XP")
        print("Completed:", self.completed)

    #When quest is completed
    def complete(self, player):
        if self.completed:
            return

        self.completed = True
        print(f"\nQuest Completed: {self.name}")
        print(f"+{self.rewardXP} XP Reward")
        player.gainXP(self.rewardXP)


    def update(self, enemyName, player):
        if self.completed or not self.unlocked or enemyName != self.targetEnemy:
            return False

        self.progress += 1
        print(f"Quest progress: {self.name} {self.progress}/{self.target}")

        if self.progress >= self.target:
            self.complete(player)
            return True

        return False
