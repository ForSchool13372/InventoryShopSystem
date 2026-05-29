from app.core.database import engine, loadPlayer, savePlayer

class PlayerRepository:
    def load(self, playerId):
        with engine.begin() as conn:
            return loadPlayer(conn, playerId)


    def save(self, playerId, player):
        with engine.begin() as conn:
            savePlayer(conn, player, playerId)