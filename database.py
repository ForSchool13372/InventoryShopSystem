from sqlalchemy import create_engine, text

#Create in memory database
engine = create_engine("sqlite:///game.db", echo = False)

def seedShop(conn):
    items = [
        ("sword", 5, 20),
        ("potion", 10, 10),
        ("garbage", 5, 5)
        ]

    for name, stock, price in items:
        conn.execute(text("""
            INSERT OR IGNORE INTO shop (itemName, stock, price)
            VALUES (:name, :stock, :price)
        """), {
                "name": name,
                "stock": stock,
                "price": price
            })

def loadPlayer(conn):
    result = conn.execute(text("SELECT gold, hp, level, xp FROM player WHERE id = 1"))
    row = result.fetchone()

    if not row:
        return None

    return {
        "gold": row[0],
        "hp": row[1],
        "level": row[2],
        "xp": row[3]
        }

def savePlayer(conn, player):
    conn.execute(text("""
        UPDATE player
        SET gold = :gold,
            hp = :hp,
            level = :level,
            xp = :xp
        WHERE id = 1
    """),{
            "gold": player.gold,
            "hp": player.hp,
            "level": player.level,
            "xp": player.xp
        })

with engine.begin() as conn:
    #Player Table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            gold INTEGER,
            hp INTEGER,
            level INTEGER,
            xp INTEGER
        )
    """))

    #Insert Player Table
    conn.execute(text("""
        INSERT OR IGNORE INTO player (gold, hp, level, xp)
        VALUES (100, 100, 1, 0)
    """))

    #Create Shop Table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS shop (
            id INTEGER PRIMARY KEY,
            itemName TEXT UNIQUE,
            stock INTEGER,
            price INTEGER
        )
    """))

    seedShop(conn)