import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setupLogger

from app.api.routes.gameController import router as apiRouter

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
# APP
# =========================
app = FastAPI()

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
# ROUTES (CORE API)
# =========================
app.include_router(apiRouter)

# =========================
# ROUTES (CACHE / INFRA)
# =========================
app.include_router(cacheRouter)

# =========================
# ROUTES (DEV ONLY)
# =========================
if DEBUG:
    from app.api.routes.devRoutes import router as devRouter
    app.include_router(devRouter)

from app.core.database import initDb

@app.on_event("startup")
async def startup():
    initDb()