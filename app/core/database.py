import os
from sqlalchemy import create_engine, text

# =========================================================
# DB ENGINE (HYBRID: SQLITE LOCAL + POSTGRES PROD)
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game.db")

engine = create_engine(DATABASE_URL, echo=False)

# =========================================================
# SEED DATA
# =========================================================
def seedShop(conn):
    items = [
        ("sword", 5, 20),
        ("potion", 10, 10),
        ("garbage", 5, 5)
    ]

    for name, stock, price in items:
        conn.execute(
            text("""
                INSERT INTO shop (itemName, stock, price)
                VALUES (:name, :stock, :price)
                ON CONFLICT (itemName)
                DO UPDATE SET
                    stock = EXCLUDED.stock,
                    price = EXCLUDED.price
            """),
            {"name": name, "stock": stock, "price": price}
        )

# =========================================================
# PLAYER FUNCTIONS
# =========================================================
def loadPlayer(conn, playerId):
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


def savePlayer(conn, player, playerId):
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
# DB INITIALIZATION
# =========================================================
with engine.begin() as conn:

    # -----------------------------------------------------
    # PLAYER TABLE
    # -----------------------------------------------------
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            gold INTEGER NOT NULL DEFAULT 100,
            hp INTEGER NOT NULL DEFAULT 100,
            level INTEGER NOT NULL DEFAULT 1,
            xp INTEGER NOT NULL DEFAULT 0
        )
    """))

    # Seed players
    for playerId in [1, 2, 3]:
        conn.execute(
            text("""
                INSERT INTO player (id, gold, hp, level, xp)
                VALUES (:id, 100, 100, 1, 0)
                ON CONFLICT (id) DO NOTHING
            """),
            {"id": playerId}
        )

    # -----------------------------------------------------
    # SHOP TABLE
    # -----------------------------------------------------
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS shop (
            id SERIAL PRIMARY KEY,
            itemName TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL,
            price INTEGER NOT NULL
        )
    """))

    # -----------------------------------------------------
    # PLAYER ITEMS TABLE (INVENTORY)
    # -----------------------------------------------------
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS playerItems (
            id SERIAL PRIMARY KEY,
            playerID INTEGER NOT NULL,
            itemName TEXT NOT NULL,
            quantity INTEGER NOT NULL,

            UNIQUE(playerID, itemName),

            FOREIGN KEY(playerID) REFERENCES player(id),
            FOREIGN KEY(itemName) REFERENCES shop(itemName)
        )
    """))

    # -----------------------------------------------------
    # SEED SHOP DATA
    # -----------------------------------------------------
    seedShop(conn)