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
                    "gold": player.gold,
                    "hp": player.hp,
                    "level": player.level,
                    "xp": player.xp,
                    "id": playerId
                }
            )

    def getAll(self):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT id, gold, hp, level, xp
                    FROM player
                """)
            ).fetchall()

            return [
                {
                    "playerId": row[0],
                    "gold": row[1],
                    "hp": row[2],
                    "level": row[3],
                    "xp": row[4]
                }
                for row in result
            ]