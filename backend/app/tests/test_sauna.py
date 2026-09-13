import pytest
from app.models.sauna import Sauna
from app.models.building import Building

@pytest.fixture
def building(db):
  building = Building(name="Viialan Kartano", address="Viialantie 666", duration_minutes=60)
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

def test_create_sauna(db, client, building):
  response = client.post(
    "/saunas",
    json={
      "name": "B2",
      "building_id": building.id
    })

  assert response.status_code == 200
  assert response.json()["name"] == "B2"
  assert response.json()["building"]["id"]

def test_get_sauna_by_id(db, client, building):
  new_sauna = client.post(
    "/saunas",
    json={
      "name": "A1",
      "building_id": building.id
    }
  )

  sauna_id = new_sauna.json()["id"]
  response = client.get(f"/saunas/{sauna_id}")

  assert response.status_code == 200
  assert response.json()["id"] == sauna_id
  assert response.json()["name"] == "A1"
  assert response.json()["building"]["id"] == building.id

def test_delete_sauna(db, client, building):
  new_sauna = client.post(
    "/saunas",
    json={
      "name": "Sauna 1",
      "building_id": building.id 
    }
  )

  sauna_id = new_sauna.json()["id"]

  response_delete = client.delete(f"/saunas/{sauna_id}")
  assert response_delete.status_code == 204

  response_get = client.get(f"/saunas/{sauna_id}")
  assert response_get.status_code == 404

def test_get_sauna_not_found(db, client):
  response = client.get("/sauna/2342342343")
  assert response.status_code == 404

def test_delete_sauna_not_found(db, client):
  response = client.delete("/saunas/37845634")
  assert response.status_code == 404

def test_create_sauna_building_not_found(db, client):
  response = client.post(
    "/saunas",
    json={
      "name": "C1",
      "building_id": 76367467
    }
  )

  assert response.status_code == 404

def test_duplicate_sauna_name(db, client, building):
  sauna1 = client.post(
    "/saunas",
    json={
      "name": "D1",
      "building_id": building.id
    }
  )

  sauna2 = client.post(
    "/saunas",
    json={
      "name": "D1",
      "building_id": sauna1.json()["building"]["id"]
    }
  )

  assert sauna2.status_code == 404
