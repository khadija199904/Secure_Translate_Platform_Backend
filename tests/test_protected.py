from fastapi.testclient import TestClient
from api_app.main import app

client = TestClient(app)

# Test accès à /translate SANS token
def test_protected_without_token():

    response = client.post("/translate?translation_sens=fr-en", json={"text": "Bonjour"})
    assert response.status_code == 401
