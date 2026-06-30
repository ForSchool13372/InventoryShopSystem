import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# =========================================================
# ENV
# =========================================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# DEBUG PRINT (ADD THIS)
print("🔥 DATABASE_URL LOADED:", DATABASE_URL)

# fallback ONLY if env missing
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///game.db"
    print("⚠️ FALLBACK: Using SQLite")

# =========================================================
# FIX: ensure sqlite works properly in CI + threads
# =========================================================
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# =========================================================
# ORM BASE
# =========================================================
Base = declarative_base()

# =========================================================
# ENGINE
# =========================================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
    connect_args=connect_args
)

# =========================================================
# INIT DB (IMPORTANT)
# =========================================================
def init_db():
    Base.metadata.create_all(bind=engine)

def getConnection():
    return engine.begin()