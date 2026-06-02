from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.cacheService import cacheService

router = APIRouter(
    prefix="/cache",
    tags=["Cache Layer"]
)


# =========================================================
# MODELS
# =========================================================

class CacheRequest(BaseModel):
    namespace: str
    key: str
    value: dict | str
    ttl: int | None = 60


# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health():
    return {
        "success": cacheService.health()
    }


# =========================================================
# SET
# =========================================================

@router.post("/set")
def setCache(data: CacheRequest):
    try:
        cacheService.set(
            data.namespace,
            data.key,
            data.value,
            data.ttl
        )

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# GET
# =========================================================

@router.get("/get")
def getCache(namespace: str, key: str):
    try:
        value = cacheService.get(namespace, key)

        return {
            "success": True,
            "cached": value is not None,
            "data": value
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))