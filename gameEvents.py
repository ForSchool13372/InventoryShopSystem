class FightWinEvent:
    def __init__(self, xp, enemy):
        self.type = "fightWin"
        self.xp = xp
        self.enemy = enemy

class FightLoseEvent:
    def __init__(self):
        self.type = "fightLose"

class EnemyKilledEvent:
    def __init__(self, enemy):
        self.type = "enemyKilled"
        self.enemy = enemy