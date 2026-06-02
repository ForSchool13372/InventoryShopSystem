from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# =========================================================
# API TESTS
# =========================================================

def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_getShop():
    response = client.get("/api/shop")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_login():
    response = client.post("/api/login", json={"playerId": 1})

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "data" in body
    assert "token" in body["data"]


def test_getPlayer():
    loginResponse = client.post("/api/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.get(
        "/api/player",
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
    loginResponse = client.post("/api/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.get(
        "/api/inventory",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "items" in body["data"]


def test_buy_invalid_quantity():
    loginResponse = client.post("/api/login", json={"playerId": 1})
    token = loginResponse.json()["data"]["token"]

    response = client.post(
        "/api/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "Potion",
            "quantity": 0
        }
    )

    assert response.status_code == 422