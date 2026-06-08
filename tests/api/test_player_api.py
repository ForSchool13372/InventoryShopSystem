def test_getPlayer(client, token):
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