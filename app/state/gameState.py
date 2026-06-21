from typing import Dict, Optional, List
from app.models.player import Player


class GameState:
    def __init__(self):
        self.players: Dict[int, Player] = {}

    # =========================================================
    # PLAYER MANAGEMENT
    # =========================================================

    def addPlayer(self, playerId: int, player: Player) -> None:
        self.players[playerId] = player

    def getPlayer(self, playerId: int) -> Optional[Player]:
        return self.players.get(playerId)

    def removePlayer(self, playerId: int) -> None:
        self.players.pop(playerId, None)

    def hasPlayer(self, playerId: int) -> bool:
        return playerId in self.players

    # =========================================================
    # LEADERBOARD (IN-MEMORY)
    # =========================================================

    def getLeaderboard(self) -> List[dict]:
        leaderboard = []

        for pid, player in self.players.items():
            stats = player.getStats()

            leaderboard.append({
                "playerId": pid,
                "gold": stats["gold"],
                "level": stats["level"],
                "hp": stats["hp"],
                "xp": stats["xp"],
            })

        # sort by level then xp
        leaderboard.sort(key=lambda x: (x["level"], x["xp"]), reverse=True)

        return leaderboard


# GLOBAL SINGLETON
gameState = GameState()