from fastapi.testclient import TestClient
from api_app.main import app

client = TestClient(app)

def test_login():
    user = {
        
  "username": "Nada",
  "password": "13456",
    
    }
    response = client.post("/login",json=user)
    assert response.status_code == 200

    json_data = response.json()
    assert "access_token" in json_data
    assert len(json_data["access_token"]) > 10
    

