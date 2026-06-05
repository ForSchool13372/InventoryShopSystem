import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
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
# ORM BASE
# =========================================================
Base = declarative_base()

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
# CONNECTION HELPER (OPTIONAL)
# =========================================================
def getConnection():
    return engine.begin()