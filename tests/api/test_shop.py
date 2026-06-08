def test_getShop(client, token):
    response = client.get(
        "/api/shop",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)


def test_buy_invalid_quantity(client, token):
    response = client.post(
        "/api/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "itemName": "Potion",
            "quantity": 0
        }
    )

    assert response.status_code == 422