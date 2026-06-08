def test_getLeaderboard(client, token):
    response = client.get(
        "/api/leaderboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    if len(body) > 0:
        first = body[0]

        assert "playerId" in first
        assert "level" in first
        assert "xp" in first
        assert "gold" in first