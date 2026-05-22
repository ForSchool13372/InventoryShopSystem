from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from typing import TypedDict, Optional

# ---------------- CONFIG ----------------

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ---------------- TOKEN PAYLOAD TYPE ----------------

class TokenPayload(TypedDict):
    playerId: int
    exp: int


# ---------------- TOKEN CREATE ----------------

def createAccessToken(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- TOKEN VERIFY ----------------

def verifyToken(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # basic safety check
        if "playerId" not in payload:
            return None

        return payload

    except JWTError:
        return None