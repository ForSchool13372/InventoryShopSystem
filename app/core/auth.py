from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from typing import TypedDict, Optional, Dict, Any

# =========================================================
# CONFIG
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================================================
# TYPE
# =========================================================

class TokenPayload(TypedDict):
    playerId: int
    exp: int


# =========================================================
# CREATE TOKEN
# =========================================================

def createAccessToken(data: Dict[str, Any]) -> str:
    """
    Create a JWT token with proper expiry handling.
    """

    toEncode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # IMPORTANT: JWT expects numeric timestamp, not datetime object
    toEncode["exp"] = int(expire.timestamp())

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


# =========================================================
# VERIFY TOKEN
# =========================================================

def verifyToken(token: str) -> Optional[TokenPayload]:
    """
    Decode and validate JWT token.
    Returns payload or None if invalid.
    """

    if not token:
        return None

    try:
        # FastAPI HTTPBearer already strips "Bearer"
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        playerId = payload.get("playerId")
        exp = payload.get("exp")

        if playerId is None or exp is None:
            return None

        # Optional: explicit expiry check (extra safety)
        if datetime.now(timezone.utc).timestamp() > int(exp):
            return None

        return {
            "playerId": int(playerId),
            "exp": int(exp)
        }

    except JWTError:
        return None
    except Exception:
        return None