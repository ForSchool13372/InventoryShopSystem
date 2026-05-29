from fastapi.testclient import TestClient
from app.api.api import app  

client = TestClient(app)

def test_getShop():
    response = client.get("/shop")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert isinstance(data["data"], list)
