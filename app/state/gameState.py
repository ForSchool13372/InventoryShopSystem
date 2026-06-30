from typing import Dict, Optional, List
from app.models.player import Player


class GameState:
    def __init__(self):
        self.players: Dict[int, Player] = {}
        self.games: Dict[int, any] = {}

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
    # SYNC HELPERS
    # =========================================================

    def updatePlayer(self, playerId: int, player: Player) -> None:
        self.players[playerId] = player

    def replaceAll(self, players: Dict[int, Player]) -> None:
        self.players = players

    # =========================================================
    # LEADERBOARD
    # =========================================================

    def getLeaderboard(self) -> List[dict]:
        leaderboard = []

        for pid, player in self.players.items():

            # Player object expected (not dict)
            core = player.core
            progression = player.progression

            leaderboard.append({
                "playerId": pid,
                "gold": core.get("gold", 0),
                "hp": core.get("hp", 0),
                "level": progression.get("level", 1),
                "xp": progression.get("xp", 0),
            })

        leaderboard.sort(
            key=lambda x: (x["level"], x["xp"]),
            reverse=True
        )

        return leaderboard


# GLOBAL SINGLETON
gameState = GameState()