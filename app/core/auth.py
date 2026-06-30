from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from typing import TypedDict, Optional, Dict, Any, cast


# =========================================================
# CONFIG
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY not set")
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
    toEncode = dict(data)

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    toEncode["exp"] = int(expire.timestamp())

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


# =========================================================
# VERIFY TOKEN (STRICTER + SAFER)
# =========================================================

def verifyToken(token: str) -> Optional[TokenPayload]:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        playerId = payload.get("playerId")
        exp = payload.get("exp")

        if not isinstance(playerId, (int, str)):
            return None

        if not isinstance(exp, (int, float)):
            return None

        if datetime.now(timezone.utc).timestamp() > float(exp):
            return None

        return cast(TokenPayload, {
            "playerId": int(playerId),
            "exp": int(exp)
        })

    except JWTError:
        return None
    except Exception:
        return None