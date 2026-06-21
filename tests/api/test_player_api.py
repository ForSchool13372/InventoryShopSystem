def test_getPlayer(client, token):
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
    assert "maxHp" in body["core"]

    # progression stats
    assert "level" in body["progression"]
    assert "xp" in body["progression"]