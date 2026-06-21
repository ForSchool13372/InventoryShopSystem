from sqlalchemy import text
from app.core.database import engine


# =========================================================
# ITEMS (SHOP SEED DATA)
# =========================================================
def createItems():
    return [
        {"itemName": "sword", "stock": 5, "price": 20},
        {"itemName": "potion", "stock": 15, "price": 5},
        {"itemName": "garbage", "stock": 10, "price": 5},
    ]


# =========================================================
# ENEMIES
# =========================================================
def createEnemies():
    return [
        {"name": "Training Dummy", "hp": 50, "xp": 30, "attack": 2, "gold": 5},
        {"name": "Goblin", "hp": 70, "xp": 50, "attack": 4, "gold": 10},
        {"name": "Slime", "hp": 40, "xp": 20, "attack": 1, "gold": 3},
        {"name": "Orc", "hp": 200, "xp": 60, "attack": 10, "gold": 10}
    ]


# =========================================================
# QUESTS
# =========================================================
def createQuests():
    quests = [
        {"title": "Kill Slimes", "target": "slime", "amount": 3, "reward": 50},
        {"title": "Kill Goblins", "target": "goblin", "amount": 2, "reward": 80},
    ]
    quests[0]["unlocked"] = True
    return quests


# =========================================================
# SHOP SEED
# =========================================================
def seedShop():
    items = createItems()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO shop ("itemName", stock, price)
                VALUES (:itemName, :stock, :price)
                ON CONFLICT ("itemName")
                DO UPDATE SET
                    stock = EXCLUDED.stock,
                    price = EXCLUDED.price
            """),
            items
        )


# =========================================================
# PLAYER SEED (ALL SAME START STATS)
# =========================================================
def seedPlayers():
    players = [
        (1, 100, 100, 100, 1, 0, 10, 5, 0.05, 1.5),
        (2, 100, 100, 100, 1, 0, 10, 5, 0.05, 1.5),
        (3, 100, 100, 100, 1, 0, 10, 5, 0.05, 1.5),
    ]

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO player (
                    id, gold, hp, "maxHp", level, xp,
                    attack, defense, "critChance", "critMultiplier"
                )
                VALUES (
                    :id, :gold, :hp, :maxHp, :level, :xp,
                    :attack, :defense, :critChance, :critMultiplier
                )
                ON CONFLICT (id)
                DO UPDATE SET
                    gold = EXCLUDED.gold,
                    hp = EXCLUDED.hp,
                    "maxHp" = EXCLUDED."maxHp",
                    level = EXCLUDED.level,
                    xp = EXCLUDED.xp,
                    attack = EXCLUDED.attack,
                    defense = EXCLUDED.defense,
                    "critChance" = EXCLUDED."critChance",
                    "critMultiplier" = EXCLUDED."critMultiplier"
            """),
            [
                {
                    "id": p[0],
                    "gold": p[1],
                    "hp": p[2],
                    "maxHp": p[3],
                    "level": p[4],
                    "xp": p[5],
                    "attack": p[6],
                    "defense": p[7],
                    "critChance": p[8],
                    "critMultiplier": p[9],
                }
                for p in players
            ]
        )


if __name__ == "__main__":
    seedPlayers()
    seedShop()
    print("Seed complete")