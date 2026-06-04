from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def ok(data):
    return {"success": True, "data": data}


def normalize(name: str):
    return name.strip().lower()


def safeExecute(func):
    try:
        return func()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unhandled error")
        raise HTTPException(status_code=500, detail="Internal server error")