class Enemy:
    def __init__(self, name, hp, xp, minDamage, maxDamage):
        self.name = name
        self.maxHp = hp
        self.hp = hp
        self.xp = xp
        self.minDamage = minDamage
        self.maxDamage = maxDamage

    def reset(self):
        self.hp = self.maxHp

    def takeDamage(self, damage):
        self.hp = max(0, self.hp - damage)