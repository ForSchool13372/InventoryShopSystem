from sqlalchemy import text
from app.core.database import engine


class QuestRepository:

    # =========================================================
    # LOAD QUESTS (GLOBAL + PLAYER PROGRESS MERGED)
    # =========================================================
    def loadQuests(self, playerId: int):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT
                    q.name,
                    q.targetenemy,
                    q.target,
                    q.rewardxp,
                    q.rewardgold,
                    COALESCE(p.progress, 0) AS progress,
                    COALESCE(p.completed, false) AS completed,
                    COALESCE(p.unlocked, false) AS unlocked,
                    COALESCE(p.claimed, false) AS claimed
                FROM quests q
                LEFT JOIN playerquests p
                    ON p.questname = q.name
                    AND p.playerid = :playerid
                ORDER BY q.name ASC
            """), {
                "playerid": playerId
            }).mappings().all()

            return rows


    # =========================================================
    # SAVE QUEST PROGRESS (FULL REWRITE)
    # =========================================================
    def saveQuests(self, playerId: int, quests):
        with engine.begin() as conn:
            conn.execute(text("""
                DELETE FROM playerquests
                WHERE playerid = :playerid
            """), {
                "playerid": playerId
            })

            for q in quests:

                questData = q if isinstance(q, dict) else {
                    "name": q.name,
                    "progress": q.progress,
                    "completed": q.completed,
                    "unlocked": q.unlocked,
                    "claimed": q.claimed
                }

                conn.execute(text("""
                    INSERT INTO playerquests (
                        playerid,
                        questname,
                        progress,
                        completed,
                        unlocked,
                        claimed
                    )
                    VALUES (
                        :playerid,
                        :questname,
                        :progress,
                        :completed,
                        :unlocked,
                        :claimed
                    )
                """), {
                    "playerid": playerId,
                    "questname": questData["name"],
                    "progress": questData["progress"],
                    "completed": questData["completed"],
                    "unlocked": questData["unlocked"],
                    "claimed": questData["claimed"]
                })