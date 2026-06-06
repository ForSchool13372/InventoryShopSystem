from sqlalchemy import text
from app.core.database import engine


class PlayerRepository:

    def load(self, playerId: int):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT gold, hp, level, xp
                    FROM player
                    WHERE id = :id
                """),
                {"id": playerId}
            ).fetchone()

            if not result:
                return None

            return {
                "gold": result[0],
                "hp": result[1],
                "level": result[2],
                "xp": result[3]
            }

    def save(self, playerId: int, player):
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE player
                    SET gold = :gold,
                        hp = :hp,
                        level = :level,
                        xp = :xp
                    WHERE id = :id
                """),
                {
                    "gold": getattr(player, "gold", player["gold"]),
                    "hp": getattr(player, "hp", player["hp"]),
                    "level": getattr(player, "level", player["level"]),
                    "xp": getattr(player, "xp", player["xp"]),
                    "id": playerId
                }
            )