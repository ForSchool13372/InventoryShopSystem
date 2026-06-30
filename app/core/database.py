import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# =========================================================
# ENV
# =========================================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game.db")

# =========================================================
# ORM BASE
# =========================================================
Base = declarative_base()

# =========================================================
# ENGINE (IMPORTANT FIX)
# =========================================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True
)

# =========================================================
# CONNECTION HELPER
# =========================================================
def getConnection():
    return engine.begin()