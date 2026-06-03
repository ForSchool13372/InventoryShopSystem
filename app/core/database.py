import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# =========================================================
# ENV
# =========================================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# fallback for local dev only
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///game.db"

# =========================================================
# ENGINE
# =========================================================
engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# =========================================================
# CONNECTION HELPER
# =========================================================
def getConnection():
    return engine.begin()

# =========================================================
# SEED DATA (SAFE / IDEMPOTENT)
# =========================================================
def seedShop(conn):
    items = [
        ("sword", 5, 20),
        ("potion", 10, 10),
        ("garbage", 5, 5)
    ]

    stmt = text("""
        INSERT INTO shop (itemName, stock, price)
        VALUES (:name, :stock, :price)
        ON CONFLICT (itemName)
        DO UPDATE SET
            stock = EXCLUDED.stock,
            price = EXCLUDED.price
    """)

    conn.execute(
        stmt,
        [{"name": n, "stock": s, "price": p} for n, s, p in items]
    )

# =========================================================
# PLAYER REPOSITORY
# =========================================================
def loadPlayer(conn, playerId: int):
    result = conn.execute(
        text("""
            SELECT gold, hp, level, xp
            FROM player
            WHERE id = :id
        """),
        {"id": playerId}
    )

    row = result.fetchone()

    if not row:
        return None

    return {
        "gold": row[0],
        "hp": row[1],
        "level": row[2],
        "xp": row[3]
    }


def savePlayer(conn, player, playerId: int):
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

# =========================================================
# DEV SEED RUNNER (OPTIONAL)
# =========================================================
def runSeed():
    with getConnection() as conn:
        seedShop(conn)


if __name__ == "__main__":
    runSeed()