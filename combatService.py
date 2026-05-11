from combat import fight

class CombatService:
    
    def handleFight(self, player, enemies):
        result = fight(player, enemies)
        return result