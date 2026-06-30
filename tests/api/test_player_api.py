import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.gameRoutes import router as gameRouter


# =========================================================
# BYPASS TEST APP (avoids main.py + circular imports)
# =========================================================
app = FastAPI()
app.include_router(gameRouter)

client = TestClient(app)


# =========================================================
# TEST
# =========================================================
def test_getPlayer(token):
    response = client.get(
        "/api/player",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    # nested structure (NEW SYSTEM)
    assert "core" in body
    assert "progression" in body
    assert "combat" in body

    # core stats
    assert "gold" in body["core"]
    assert "hp" in body["core"]
    assert "maxhp" in body["core"]

    # progression stats
    assert "level" in body["progression"]
    assert "xp" in body["progression"]