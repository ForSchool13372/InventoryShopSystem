from sqlalchemy import text
from app.core.database import engine


class PlayerRepository:

    # =========================================================
    # LOAD (DB -> Python)
    # =========================================================
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

            return self._mapRow(result)

    # =========================================================
    # SAVE (Python -> DB)
    # =========================================================
    def save(self, playerId: int, player):
        data = player.toDict()

        params = {
            "id": playerId,

            # core
            "gold": data.get("gold"),
            "hp": data.get("hp"),
            "maxhp": data.get("maxhp"),

            # progression
            "level": data.get("level"),
            "xp": data.get("xp"),

            # combat
            "attack": data.get("attack"),
            "defense": data.get("defense"),
            "critchance": data.get("critchance"),
            "critmultiplier": data.get("critmultiplier"),
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
                params
            )

    # =========================================================
    # GET ALL (DB -> Python)
    # =========================================================
    def getAll(self):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT *
                    FROM player
                """)
            ).mappings().all()

            return [self._mapRow(row) for row in result]

    # =========================================================
    # MAPPER (DB -> Python format)
    # =========================================================
    def _mapRow(self, row):
        rowDict = dict(row)

        return {
            "id": rowDict.get("id"),
            "gold": rowDict.get("gold"),
            "hp": rowDict.get("hp"),
            "maxhp": rowDict.get("maxhp"),

            "level": rowDict.get("level"),
            "xp": rowDict.get("xp"),

            "attack": rowDict.get("attack"),
            "defense": rowDict.get("defense"),

            "critChance": rowDict.get("critchance"),
            "critMultiplier": rowDict.get("critmultiplier"),
        }