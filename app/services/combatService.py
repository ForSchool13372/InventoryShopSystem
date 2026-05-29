class CombatService:

    def handleFight(self, player, enemies):
        result = self._executeFight(player, enemies)
        return result

    # =========================================================
    # INTERNAL DOMAIN CALL
    # =========================================================

    def _executeFight(self, player, enemies):
        from combat import fight
        return fight(player, enemies)