def test_login(client):
    response = client.post("/api/login", json={"playerId": 1})

    assert response.status_code == 200
    assert "token" in response.json()


def test_missing_token_fails(client):
    response = client.get("/api/player")
    assert response.status_code == 401