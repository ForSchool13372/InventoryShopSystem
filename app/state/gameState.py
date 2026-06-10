from typing import Dict
from app.models.player import Player


class GameState:
    def __init__(self):
        self.players: Dict[int, Player] = {}

    # -----------------------------
    # LOAD / REGISTER PLAYER
    # -----------------------------
    def addPlayer(self, playerId: int, player: Player):
        self.players[playerId] = player

    def getPlayer(self, playerId: int) -> Player:
        return self.players.get(playerId)

    def removePlayer(self, playerId: int):
        if playerId in self.players:
            del self.players[playerId]

    # -----------------------------
    # LEADERBOARD SOURCE
    # -----------------------------
    def getLeaderboard(self):
        return [
            {
                "playerId": pid,
                **player.getStats()
            }
            for pid, player in self.players.items()
        ]


# GLOBAL SINGLETON
gameState = GameState()