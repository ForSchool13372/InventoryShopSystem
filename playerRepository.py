from database import engine, loadPlayer, savePlayer

class PlayerRepository:
    def load(self, playerId):
        with engine.begin() as conn:
            data = loadPlayer(conn, playerId)

        if not data:
            return None

        return data

    def save(self, playerId, player):
        with engine.begin() as conn:
            savePlayer(conn, player, playerId)