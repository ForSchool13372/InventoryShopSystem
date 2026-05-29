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
    toEncode = data.copy()

    # safer + standard JWT expiry (no manual timestamp casting)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode["exp"] = expire

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


# =========================================================
# VERIFY TOKEN
# =========================================================

def verifyToken(token: str) -> Optional[TokenPayload]:
    try:
        # handle "Bearer <token>" case safely
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        playerId = payload.get("playerId")
        exp = payload.get("exp")

        if playerId is None or exp is None:
            return None

        return {
            "playerId": int(playerId),
            "exp": int(exp)
        }

    except JWTError:
        return None
    except Exception:
        # prevents random crashes from breaking CORS / FastAPI
        return None