class CombatService:
    def __init__(self, combatEngine=None):
        """
        combatEngine is optional so we can inject or mock it in tests.
        If not provided, we import the real fight function.
        """
        if combatEngine is None:
            from app.services.combat import fight
            combatEngine = fight

        self.combatEngine = combatEngine

    # =========================================================
    # PUBLIC API
    # =========================================================

    def handleFight(self, player, enemies):
        """
        Main entry point for combat.
        Returns result of fight.
        """
        return self.combatEngine(player, enemies)