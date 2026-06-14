import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setupLogger
from app.core.redisClient import initRedis
from app.api.routes.gameRoutes import router as gameRouter
from app.api.routes.cacheRoutes import router as cacheRouter

# =========================
# ENV CONFIG
# =========================
ENV = os.getenv("ENV", "prod").lower()
DEBUG = ENV == "dev"

# =========================
# INIT LOGGING
# =========================
setupLogger()

# =========================
# LIFESPAN (STARTUP/SHUTDOWN)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    initRedis()
    yield
    # shutdown (optional cleanup later)

# =========================
# APP
# =========================
app = FastAPI(lifespan=lifespan)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://inventoryshopsystem.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES
# =========================
app.include_router(gameRouter)
app.include_router(cacheRouter)

# =========================
# DEV ONLY ROUTES
# =========================
if DEBUG:
    from app.api.routes.devRoutes import router as devRouter
    app.include_router(devRouter)