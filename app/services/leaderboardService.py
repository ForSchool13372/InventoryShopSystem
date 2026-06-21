class LeaderboardService:
    def __init__(self, playerRepo):
        self.playerRepo = playerRepo

    def getLeaderboard(self):
        allPlayers = self.playerRepo.getAll()

        sortedPlayers = sorted(
            allPlayers,
            key=lambda p: (
                p.get("level", 1),
                p.get("xp", 0),
                p.get("gold", 0)
            ),
            reverse=True
        )

        return [
            {
                "playerId": p["id"],  
                "level": p.get("level", 1),
                "xp": p.get("xp", 0),
                "gold": p.get("gold", 0)
            }
            for p in sortedPlayers
        ]