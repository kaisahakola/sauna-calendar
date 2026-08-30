from app.models.building import Building

def test_get_buildings(db, client):
  db_building = Building(address="Siurontie 18", name="Siuron Kartano")
  db.add(db_building)
  db.commit()

  response = client.get("/buildings")
  assert response.status_code == 200
  assert response.json()[0]["name"] == "Siuron Kartano"
  assert response.json()[0]["address"] == "Siurontie 18"

def test_create_building(db,client):
  response = client.post(
    "/buildings",
    json={
      "name": "Siuron Kartano",
      "address": "Siurontie 25"
    }
  )

  assert response.status_code == 200
  assert response.json()["name"] == "Siuron Kartano"
  assert response.json()["address"] == "Siurontie 25"

def test_get_building_by_id(db, client):
  new_building = client.post(
    "/buildings",
    json={
      "name": "Kaukajärven Kartano",
      "address": "Kaukajärventie 25"
    }
  )

  building_id = new_building.json()["id"]
  response = client.get(f"/buildings/{building_id}")

  assert response.status_code == 200
  assert response.json()["id"] == building_id
  assert response.json()["name"] == "Kaukajärven Kartano"
  assert response.json()["address"] == "Kaukajärventie 25"

def test_delete_building(db, client):
  new_building = client.post(
    "/buildings",
    json={
      "name": "Espoon Kartano",
      "address": "Espoontie 25"
    }
  )

  building_id = new_building.json()["id"]

  response_delete = client.delete(f"/buildings/{building_id}")
  assert response_delete.status_code == 204

  response_get = client.get(f"/buildings/{building_id}")
  assert response_get.status_code == 404

def test_get_building_not_found(db, client):
  response = client.get("buildings/23424234")

  assert response.status_code == 404

def test_delete_building_not_found(db, client):
  response = client.delete("buildings/76765473")

  assert response.status_code == 404
