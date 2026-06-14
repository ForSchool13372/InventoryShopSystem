from app.core.database import Base
from sqlalchemy import Column, Integer, String


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    gold = Column(Integer, default=0)
    hp = Column(Integer, default=100)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)

    itemName = Column(String, unique=True, nullable=False)

    stock = Column(Integer, default=0)
    price = Column(Integer, default=0)