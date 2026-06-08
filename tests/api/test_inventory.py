def test_getInventory(client, token):
    response = client.get(
        "/api/inventory",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "items" in body