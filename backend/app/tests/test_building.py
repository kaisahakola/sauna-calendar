from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_buildings():
  response = client.get("/buildings")
  assert response.status_code == 200
