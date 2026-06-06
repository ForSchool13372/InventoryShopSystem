from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# =========================================================
# HELPERS
# =========================================================

def get_token():
    response = client.post("/api/login", json={"playerId": 1})
    return response.json()["token"]

# =========================================================
# API TESTS
# =========================================================

def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_getShop():
    token = get_token()

    response = client.get(
        "/api/shop",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)


def test_login():
    response = client.post("/api/login", json={"playerId": 1})

    assert response.status_code == 200

    body = response.json()

    assert "token" in body
    assert "id" in body


def test_getPlayer():
    token = get_token()

    response = client.get(
        "/api/player",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "gold" in body
    assert "hp" in body
    assert "level" in body
    assert "xp" in body


def test_getInventory():
    token = get_token()

    response = client.get(
        "/api/inventory",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "items" in body


def test_buy_invalid_quantity():
    token = get_token()

    response = client.post(
        "/api/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "Potion",
            "quantity": 0
        }
    )

    assert response.status_code == 422