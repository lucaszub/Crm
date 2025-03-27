from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_client():
    response = client.post("/clients", json={
        "id": "4",
        "name": "Test Client",
        "entreprise": "Test Entreprise",
        "role": "Test Role",
        "status": "Test Status",
        "email": "test.client@example.com",
        "numero": "1234567890",
        "avatarUrl": "",
        "interaction": "01/01/2025"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Client"