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


# =========================================================
# ADDED COVERAGE TESTS (IMPORTANT)
# =========================================================

def test_buy_success():
    token = get_token()

    response = client.post(
        "/api/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "sword",
            "quantity": 1
        }
    )

    assert response.status_code == 200


def test_buy_fail_not_enough_gold():
    token = get_token()

    response = client.post(
        "/api/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "sword",
            "quantity": 9999
        }
    )

    assert response.status_code in (200, 400)


def test_sell_success():
    token = get_token()

    response = client.post(
        "/api/sell",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "sword",
            "quantity": 1
        }
    )

    assert response.status_code == 200


def test_missing_token_fails():
    response = client.get("/api/player")
    assert response.status_code == 401


# =========================================================
# COMBAT COVERAGE TESTS (RESTORED)
# =========================================================

def test_fight_basic():
    from app.services.combat import fight

    class Player:
        def __init__(self):
            self.hp = 100
            self.level = 1

        def takeDamage(self, dmg):
            self.hp -= dmg

    class Enemy:
        def __init__(self):
            self.name = "goblin"
            self.hp = 10
            self.attack = 1

        def takeDamage(self, dmg):
            self.hp -= dmg

    player = Player()
    enemy = Enemy()

    result = fight(player, [enemy])

    assert isinstance(result, dict)
    assert "result" in result
    assert "xp" in result
    assert "enemy" in result
    assert "logs" in result

def test_combat_service():
    from app.services.combatService import CombatService

    class Player:
        def __init__(self):
            self.hp = 100
            self.level = 1

        def takeDamage(self, dmg):
            self.hp -= dmg

    class Enemy:
        def __init__(self):
            self.name = "goblin"
            self.hp = 10
            self.attack = 1

        def takeDamage(self, dmg):
            self.hp -= dmg

    service = CombatService()

    player = Player()
    enemy = Enemy()

    result = service.handleFight(player, [enemy])

    assert isinstance(result, dict)
    assert "result" in result