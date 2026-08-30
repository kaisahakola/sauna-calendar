import pytest
from app.models.sauna import Sauna
from app.models.building import Building

@pytest.fixture
def building(db):
  building = Building(name="Viialan Kartano", address="Viialantie 666")
  db.add(building)
  db.commit()
  db.refresh(building)

  return building

def test_get_saunas(db, client, building):
  sauna = Sauna(name="A1", building_id=building.id)
  db.add(sauna)
  db.commit()

  response = client.get("/saunas")
  assert response.status_code == 200
  assert response.json()[0]["name"] == "A1"

def test_create_building(db, client, building):
  response = client.post(
    "/saunas",
    json={
      "name": "B2",
      "building_id": building.id
    })

  assert response.status_code == 200
  assert response.json()["name"] == "B2"
  assert response.json()["building"]["id"]
