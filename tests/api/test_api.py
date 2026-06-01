from fastapi.testclient import TestClient
from app.api.api import app

# =========================================================
# SETUP
# =========================================================
client = TestClient(app)

# =========================================================
# API TESTS
# =========================================================

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_getShop():
    response = client.get("/shop")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_login():
    response = client.post("/login", json={"playerId": 1})

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "data" in body
    assert "token" in body["data"]


def test_getPlayer():
    loginResponse = client.post("/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.get(
        "/player",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "gold" in body["data"]
    assert "hp" in body["data"]
    assert "level" in body["data"]
    assert "xp" in body["data"]


def test_getInventory():
    loginResponse = client.post("/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.get(
        "/inventory",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "items" in body["data"]


def test_buy_invalid_quantity():
    loginResponse = client.post("/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.post(
        "/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "Potion",
            "quantity": 0
        }
    )

    assert response.status_code == 422