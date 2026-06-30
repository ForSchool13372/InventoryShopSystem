from app.core.database import Base
from sqlalchemy import Column, Integer, String


# =========================================================
# PLAYER TABLE
# =========================================================
class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)

    gold = Column(Integer, default=0)
    hp = Column(Integer, default=100)
    maxHp = Column(Integer, default=100)

    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)

    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)

    critChance = Column(Integer, default=5)  
    critMultiplier = Column(Integer, default=2)


# =========================================================
# SHOP TABLE
# =========================================================
class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)

    itemName = Column(String, unique=True, nullable=False)

    stock = Column(Integer, default=0)
    price = Column(Integer, default=0)


# =========================================================
# PLAYER ITEMS (INVENTORY TABLE)
# =========================================================
class PlayerItems(Base):
    __tablename__ = "playerItems"

    playerID = Column(Integer, primary_key=True)
    itemName = Column(String, primary_key=True)

    quantity = Column(Integer, default=0)