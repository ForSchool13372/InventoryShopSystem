import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setupLogger
from app.api.routes import router

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
# ROUTES (ALWAYS AVAILABLE)
# =========================
app.include_router(router)

# =========================
# ROUTES (DEV ONLY)
# =========================
if DEBUG:
    from app.api.devRoutes import router as devRouter

    app.include_router(devRouter)