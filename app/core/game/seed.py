from sqlalchemy import text
from app.core.database import engine
from app.models.enemy import Enemy


# =========================================================
# ITEMS (SHOP SEED DATA)
# =========================================================
def createItems():
    return [
        {
            "itemname": "sword",
            "stock": 5,
            "price": 20,
            "itemtype": "weapon",
            "description": "A basic iron sword.",
            "rarity": "common"
        },
        {
            "itemname": "potion",
            "stock": 15,
            "price": 5,
            "itemtype": "consumable",
            "description": "Restores a small amount of HP.",
            "rarity": "common"
        },
        {
            "itemname": "garbage",
            "stock": 10,
            "price": 5,
            "itemtype": "junk",
            "description": "Useless junk. Might be valuable to someone?",
            "rarity": "trash"
        },
    ]


# =========================================================
# ENEMIES
# =========================================================
def createEnemies():
    return [
        Enemy("Training Dummy", 50, 30, 5, 2, 4),
        Enemy("Goblin", 70, 50, 10, 4, 8),
        Enemy("Slime", 40, 20, 3, 1, 3),
        Enemy("Orc", 200, 60, 10, 8, 15)
    ]


# =========================================================
# QUESTS
# =========================================================
def createQuests():
    return [
        {
            "name": "Goblin Hunt",
            "targetEnemy": "goblin",
            "target": 2,
            "rewardXP": 80,
            "rewardGold": 40
        },
        {
            "name": "Slime Infestation",
            "targetEnemy": "slime",
            "target": 3,
            "rewardXP": 50,
            "rewardGold": 20
        }
    ]


# =========================================================
# SHOP SEED (SAFE UPSERT)
# =========================================================
def seedShop():
    items = createItems()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO shop (
                    itemname, stock, price,
                    itemtype, description, rarity
                )
                VALUES (
                    :itemname, :stock, :price,
                    :itemtype, :description, :rarity
                )
                ON CONFLICT (itemname)
                DO UPDATE SET
                    stock = EXCLUDED.stock,
                    price = EXCLUDED.price,
                    itemtype = EXCLUDED.itemtype,
                    description = EXCLUDED.description,
                    rarity = EXCLUDED.rarity
            """),
            items
        )


# =========================================================
# PLAYER SEED (SAFE UPSERT)
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
                    id, gold, hp, maxhp, level, xp,
                    attack, defense, critchance, critmultiplier
                )
                VALUES (
                    :id, :gold, :hp, :maxhp, :level, :xp,
                    :attack, :defense, :critchance, :critmultiplier
                )
                ON CONFLICT (id)
                DO UPDATE SET
                    gold = EXCLUDED.gold,
                    hp = EXCLUDED.hp,
                    maxhp = EXCLUDED.maxhp,
                    level = EXCLUDED.level,
                    xp = EXCLUDED.xp,
                    attack = EXCLUDED.attack,
                    defense = EXCLUDED.defense,
                    critchance = EXCLUDED.critchance,
                    critmultiplier = EXCLUDED.critmultiplier
            """),
            [
                {
                    "id": p[0],
                    "gold": p[1],
                    "hp": p[2],
                    "maxhp": p[3],
                    "level": p[4],
                    "xp": p[5],
                    "attack": p[6],
                    "defense": p[7],
                    "critchance": p[8],
                    "critmultiplier": p[9],
                }
                for p in players
            ]
        )


# =========================================================
# QUEST SEED (UPSERT FIXED)
# =========================================================
def seedQuests():
    quests = createQuests()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO quests (
                    name, targetenemy, target, rewardxp, rewardgold
                )
                VALUES (
                    :name, :targetEnemy, :target, :rewardXP, :rewardGold
                )
                ON CONFLICT (name)
                DO UPDATE SET
                    targetenemy = EXCLUDED.targetenemy,
                    target = EXCLUDED.target,
                    rewardxp = EXCLUDED.rewardxp,
                    rewardgold = EXCLUDED.rewardgold
            """),
            quests
        )


# =========================================================
# PLAYER QUEST SEED (UPSERT FIXED)
# =========================================================
def seedPlayerQuests():
    quests = createQuests()
    playerIds = [1, 2, 3]

    with engine.begin() as conn:
        for pid in playerIds:
            for q in quests:
                conn.execute(
                    text("""
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
                            0,
                            false,
                            :unlocked,
                            false
                        )
                        ON CONFLICT (playerid, questname)
                        DO UPDATE SET
                            unlocked = EXCLUDED.unlocked
                    """),
                    {
                        "playerid": pid,
                        "questname": q["name"],
                        "unlocked": True if q["name"] == "Goblin Hunt" else False
                    }
                )


# =========================================================
# MAIN SEED RUNNER
# =========================================================
if __name__ == "__main__":
    seedPlayers()
    seedShop()
    seedQuests()
    seedPlayerQuests()
    print("Seed complete")