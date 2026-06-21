from sqlalchemy import text
from app.core.database import engine


class PlayerRepository:

    def load(self, playerId: int):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT *
                    FROM player
                    WHERE id = :id
                """),
                {"id": playerId}
            ).mappings().fetchone()

            if not result:
                return None

            return dict(result)


    def save(self, playerId: int, player):
        data = player.toDict()

        data = {
            "gold": data.get("gold", 0),
            "hp": data.get("hp", 100),
            "maxhp": data.get("maxHp", 100),

            "level": data.get("level", 1),
            "xp": data.get("xp", 0),

            "attack": data.get("attack", 10),
            "defense": data.get("defense", 5),

            "critchance": data.get("critChance", 0.05),
            "critmultiplier": data.get("critMultiplier", 1.5),
        }

        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE player
                    SET gold = :gold,
                        hp = :hp,
                        maxhp = :maxhp,
                        level = :level,
                        xp = :xp,
                        attack = :attack,
                        defense = :defense,
                        critchance = :critchance,
                        critmultiplier = :critmultiplier
                    WHERE id = :id
                """),
                {"id": playerId, **data}
            )


    def getAll(self):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT *
                    FROM player
                """)
            ).mappings().all()

            return [dict(row) for row in result]